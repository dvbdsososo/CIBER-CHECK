
from puntaje import calcular_puntaje

IDS = [
    "https",
    "redireccion_https",
    "certificado_valido",
    "header_csp",
    "header_hsts",
    "header_xframe",
    "header_xcontent",
    "info_servidor"
]


def hacer_datos(fallan):
    return {
        "url": "https://prueba.test",
        "resultados": [
            {"id": i, "ok": i not in fallan}
            for i in IDS
        ]
    }


CASOS = [
    ("perfecto", [], 100, "A"),
    (
        "regular",
        ["header_csp", "header_hsts", "header_xframe",
         "info_servidor"],
        70,
        "C"
    ),
    ("malo", IDS, 10, "F")
]


for nombre, fallan, puntos, calificacion in CASOS:
    resultado = calcular_puntaje(hacer_datos(fallan))

    correcto = (
        resultado["puntaje"] == puntos
        and resultado["calificacion"] == calificacion
    )

    print(
        nombre,
        resultado["puntaje"],
        resultado["calificacion"],
        "OK" if correcto else "REVISAR"
    )
