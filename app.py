import requests
from flask import Flask, render_template, request

from escaner import revisar_sitio
from puntaje import calcular_puntaje

app = Flask(__name__)


def normalizar(url):
    """Si el usuario no escribió http:// o https://, agregamos https://."""
    url = url.strip()
    if not url.lower().startswith(("http://", "https://")):
        url = "https://" + url
    return url


def sitio_responde(url):
    """Revisa que el sitio conteste antes de calificarlo."""
    try:
        requests.get(url, timeout=10, verify=False)
        return True
    except requests.RequestException:
        return False


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/analizar", methods=["POST"])
def analizar():
    texto = request.form.get("url", "").strip()

    if not texto:
        return render_template(
            "index.html",
            error="Escribe el link de un sitio para analizarlo."
        ), 400

    url = normalizar(texto)

    if not sitio_responde(url):
        return render_template(
            "index.html",
            url=texto,
            error="No pudimos conectar con ese sitio. Revisa que el link "
                  "esté bien escrito. Si el sitio no tiene HTTPS, "
                  "escribe http:// al inicio."
        ), 400

    try:
        datos = revisar_sitio(url)
        resultado = calcular_puntaje(datos)
    except Exception:
        return render_template(
            "index.html",
            url=texto,
            error="Algo falló al analizar el sitio. Intenta de nuevo."
        ), 500

    return render_template("resultado.html", url=url, r=resultado)


if __name__ == "__main__":
    # debug=True solo para desarrollo: quítenlo si publican la página.
    app.run(debug=True)
