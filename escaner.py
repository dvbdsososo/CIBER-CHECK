import json
import sys
import requests
import urllib3

urllib3.disable_warnings()   # evita avisos de certificado
TIMEOUT = 10                 # segundos máximos de espera


def revisar_sitio(url):
    resultados = []

    def agregar(id_, ok):
        resultados.append({"id": id_, "ok": ok})

    es_https = url.startswith("https://")

    # 1. ¿usa HTTPS?
    agregar("https", es_https)

    # 2. ¿HTTP redirige a HTTPS?
    try:
        url_http = "http://" + url.split("://")[-1]
        r = requests.get(url_http, timeout=TIMEOUT)
        agregar("redireccion_https", r.url.startswith("https://"))
    except requests.RequestException:
        agregar("redireccion_https", False)

    # 3. ¿el certificado es válido?
    if es_https:
        try:
            requests.get(url, timeout=TIMEOUT, verify=True)
            agregar("certificado_valido", True)
        except requests.RequestException:
            agregar("certificado_valido", False)
    else:
        agregar("certificado_valido", False)
    # Descargamos la página una vez para leer sus headers
    try:
        resp = requests.get(url, timeout=TIMEOUT, verify=False)
        h = resp.headers
    except requests.RequestException:
        h = {}

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