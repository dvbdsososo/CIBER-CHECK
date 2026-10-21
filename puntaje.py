
import json
import os

RUTA = os.path.join(os.path.dirname(__file__), "reglas.json")

with open(RUTA, encoding="utf-8") as f:
    REGLAS = json.load(f)

ORDEN = {"alta": 0, "media": 1, "baja": 2}


def letra(puntaje):
    if puntaje >= 90:
        return "A"
    if puntaje >= 80:
        return "B"
    if puntaje >= 70:
        return "C"
    if puntaje >= 60:
        return "D"
    return "F"


def calcular_puntaje(datos):
    puntaje = 100
    problemas = []

    for r in datos["resultados"]:
        if not r["ok"] and r["id"] in REGLAS:
            regla = REGLAS[r["id"]]
            puntaje -= regla["puntos"]
            problemas.append({"id": r["id"], **regla})

    puntaje = max(puntaje, 0)
    problemas.sort(key=lambda p: ORDEN[p["gravedad"]])

    return {
        "puntaje": puntaje,
        "calificacion": letra(puntaje),
        "problemas": problemas
    }
