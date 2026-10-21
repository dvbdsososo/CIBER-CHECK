import json
import sys
import requests
import urllib3

urllib3.disable_warnings()   # evita avisos de certificado
TIMEOUT = 10                 # segundos máximos de espera

IDS = ["https", "redireccion_https", "certificado_valido", "header_csp",
       "header_hsts", "header_xframe", "header_xcontent", "info_servidor"]


def revisar_sitio(url):
    resultados = []

    def agregar(id_, ok):
        resultados.append({"id": id_, "ok": ok})

    # Primero vemos si el sitio responde. Si no, no se puede revisar nada
    # y todo se manda como None (no se pudo verificar).
    try:
        resp = requests.get(url, timeout=TIMEOUT, verify=False)
        h = resp.headers
    except requests.RequestException:
        return {"url": url, "resultados": [{"id": i, "ok": None} for i in IDS]}

    url_final = resp.url                      # por si el sitio redirige
    es_https = url_final.startswith("https://")

    # 1. ¿usa HTTPS?
    agregar("https", es_https)

    # 2. ¿HTTP redirige a HTTPS?
    try:
        url_http = "http://" + url_final.split("://")[-1]
        r = requests.get(url_http, timeout=TIMEOUT)
        agregar("redireccion_https", r.url.startswith("https://"))
    except requests.RequestException:
        agregar("redireccion_https", None)

    # 3. ¿el certificado es válido?
    if es_https:
        try:
            requests.get(url_final, timeout=TIMEOUT, verify=True)
            agregar("certificado_valido", True)
        except requests.exceptions.SSLError:
            agregar("certificado_valido", False)
        except requests.RequestException:
            agregar("certificado_valido", None)
    else:
        agregar("certificado_valido", False)

    # 4 a 7. Headers de seguridad (ok = el header existe)
    agregar("header_csp", "Content-Security-Policy" in h)
    agregar("header_hsts", "Strict-Transport-Security" in h)
    agregar("header_xframe", "X-Frame-Options" in h)
    agregar("header_xcontent", "X-Content-Type-Options" in h)

    # 8. ¿expone la versión del servidor? (ok = NO la expone)
    servidor = h.get("Server", "")
    expone = ("X-Powered-By" in h) or any(c.isdigit() for c in servidor)
    agregar("info_servidor", not expone)

    return {"url": url, "resultados": resultados}


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    print(json.dumps(revisar_sitio(url), indent=2, ensure_ascii=False))