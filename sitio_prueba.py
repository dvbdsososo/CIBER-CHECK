from flask import Flask

app = Flask(__name__)


@app.route("/")
def inicio():
    return "<h1>Sitio de prueba</h1><p>Inseguro a propósito.</p>"


@app.after_request
def agregar_headers(resp):
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    return resp


if __name__ == "__main__":
    app.run(port=8000)