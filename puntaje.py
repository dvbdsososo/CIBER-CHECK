

import json
import os

RUTA = os.path.join(os.path.dirname(__file__), "reglas.json")

ORDEN = {"alta": 0, "media": 1, "baja": 2}
CAMPOS = ("titulo", "gravedad", "puntos", "explicacion", "sugerencia")


def validar_reglas(reglas):
    """Revisa que cada regla tenga todos sus campos y una gravedad válida."""
    for id_regla, regla in reglas.items():
        faltan = [c for c in CAMPOS if c not in regla]
        if faltan:
            raise ValueError(f"La regla '{id_regla}' no tiene los campos: {', '.join(faltan)}")
        if regla["gravedad"] not in ORDEN:
            raise ValueError(
                f"La regla '{id_regla}' tiene gravedad '{regla['gravedad']}'. "
                "Debe ser alta, media o baja."
            )
        puntos = regla["puntos"]
        if isinstance(puntos, bool) or not isinstance(puntos, (int, float)):
            raise ValueError(f"La regla '{id_regla}' tiene 'puntos' que no es un número.")


with open(RUTA, encoding="utf-8") as f:
    REGLAS = json.load(f)

validar_reglas(REGLAS)


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
    no_verificados = []
    vistos = set()

    # Si faltan los resultados (o no son una lista), se tratan como vacíos
    resultados = datos.get("resultados") if isinstance(datos, dict) else None
    if not isinstance(resultados, list):
        resultados = []

    for r in resultados:
        # Ignorar entradas incompletas o con formato raro
        if not isinstance(r, dict) or "ok" not in r:
            continue
        id_regla = r.get("id")
        if not isinstance(id_regla, str):
            continue

        # Ignorar ids repetidos para no restar dos veces
        if id_regla in vistos:
            continue
        vistos.add(id_regla)

        if id_regla not in REGLAS:
            continue

        ok = r["ok"]

        # ok = null: la revisión no se pudo hacer, así que no se descuenta
        if ok is None:
            no_verificados.append(id_regla)
            continue

        if not ok:
            regla = REGLAS[id_regla]
            puntaje -= regla["puntos"]
            problemas.append({"id": id_regla, **regla})

    puntaje = max(puntaje, 0)
    problemas.sort(key=lambda p: ORDEN[p["gravedad"]])

    return {
        "puntaje": puntaje,
        "calificacion": letra(puntaje),
        "problemas": problemas,
        "no_verificados": no_verificados
    }