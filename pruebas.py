import re
import sys

from puntaje import calcular_puntaje, REGLAS, CAMPOS

# Los ids salen de reglas.json, así que una regla nueva entra sola a las pruebas
IDS = list(REGLAS)

CAMPOS_TEXTO = ("titulo", "explicacion", "sugerencia")
MAX_ORACIONES = 2


def hacer_datos(fallan):
    return {
        "url": "https://prueba.test",
        "resultados": [
            {"id": i, "ok": i not in fallan}
            for i in IDS
        ]
    }


def puntaje_esperado(fallan):
    """Calcula el puntaje con los puntos de reglas.json, sin números fijos."""
    return max(100 - sum(REGLAS[i]["puntos"] for i in fallan), 0)


def letra_esperada(puntaje):
    for minimo, letra in ((90, "A"), (80, "B"), (70, "C"), (60, "D")):
        if puntaje >= minimo:
            return letra
    return "F"


def contar_oraciones(texto):
    partes = re.split(r"(?<=[.!?])\s+", texto.strip())
    return len([p for p in partes if p])


CASOS = [
    ("perfecto", []),
    ("regular", ["header_csp", "header_hsts", "header_xframe", "info_servidor"]),
    ("malo", IDS),
]

hubo_errores = False

# Prueba de puntajes
for nombre, fallan in CASOS:
    resultado = calcular_puntaje(hacer_datos(fallan))
    puntos = puntaje_esperado(fallan)

    correcto = (
        resultado["puntaje"] == puntos
        and resultado["calificacion"] == letra_esperada(puntos)
    )
    hubo_errores |= not correcto

    print(
        nombre,
        resultado["puntaje"],
        resultado["calificacion"],
        "OK" if correcto else "REVISAR"
    )

# Prueba de textos: sin campos faltantes y máximo 2 oraciones
for id_regla, regla in REGLAS.items():
    problemas = []

    for campo in CAMPOS:
        if campo not in regla:
            problemas.append(f"falta el campo '{campo}'")

    for campo in CAMPOS_TEXTO:
        texto = regla.get(campo)
        if not isinstance(texto, str) or not texto.strip():
            problemas.append(f"'{campo}' está vacío")
        elif contar_oraciones(texto) > MAX_ORACIONES:
            problemas.append(
                f"'{campo}' tiene {contar_oraciones(texto)} oraciones "
                f"(máximo {MAX_ORACIONES})"
            )

    hubo_errores |= bool(problemas)
    print(f"texto {id_regla}", "OK" if not problemas else "REVISAR: " + "; ".join(problemas))

sys.exit(1 if hubo_errores else 0)