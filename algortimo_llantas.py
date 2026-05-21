# ==========================================
# Archivo principal: AEstrella_Llantas.py
# ==========================================

from arbol import Nodo

# ------------------------------------------
# TABLA DE COSTOS
# ------------------------------------------

costos = {
    "Empresa 1": {"T": 20, "H": 30, "V": 20, "W": 40},
    "Empresa 2": {"T": 50, "H": 50, "V": 40, "W": 50},
    "Empresa 3": {"T": 60, "H": 55, "V": 50, "W": 60},
    "Empresa 4": {"T": 100, "H": 80, "V": 60, "W": 70}
}

tipos_llantas = ["T", "H", "V", "W"]


# ------------------------------------------
# HEURISTICA h(n)
# ------------------------------------------

def heuristica(asignacion_actual, empresas_usadas, costos_base=None):

    if costos_base is None:
        costos_base = costos

    llantas_restantes = []

    for llanta in tipos_llantas:
        if llanta not in asignacion_actual:
            llantas_restantes.append(llanta)

    empresas_restantes = []

    for empresa in costos:
        if empresa not in empresas_usadas:
            empresas_restantes.append(empresa)

    h = 0

    for llanta in llantas_restantes:

        minimo = float("inf")

        for empresa in empresas_restantes:

            precio = costos_base[empresa][llanta]

            if precio < minimo:
                minimo = precio

        h += minimo

    return h


# ------------------------------------------
# f(n)=g(n)+h(n)
# ------------------------------------------

def costo_estimado(nodo, costos_base=None):

    if costos_base is None:
        costos_base = costos

    datos = nodo.get_datos()

    asignacion = datos["asignacion"]
    usadas = datos["usadas"]

    g = nodo.get_costo()

    h = heuristica(asignacion, usadas, costos_base)

    return g + h


# ------------------------------------------
# ALGORITMO A*
# ------------------------------------------

def buscar_solucion_Aestrella(costos_base=None):

    if costos_base is None:
        costos_base = costos

    nodos_visitados = []
    nodos_frontera = []

    estado_inicial = {
        "asignacion": {},
        "usadas": []
    }

    nodo_inicial = Nodo(estado_inicial)

    nodo_inicial.set_costo(0)

    nodos_frontera.append(nodo_inicial)

    while len(nodos_frontera) != 0:

        nodos_frontera = sorted(
            nodos_frontera,
            key=lambda nodo: costo_estimado(nodo, costos_base)
        )

        nodo_actual = nodos_frontera.pop(0)

        nodos_visitados.append(nodo_actual)

        # SOLUCION
        if len(nodo_actual.get_datos()["asignacion"]) == 4:
            return nodo_actual

        asignacion_actual = nodo_actual.get_datos()["asignacion"]
        empresas_usadas = nodo_actual.get_datos()["usadas"]

        siguiente_llanta = tipos_llantas[len(asignacion_actual)]

        lista_hijos = []

        for empresa in costos_base:

            if empresa not in empresas_usadas:

                nueva_asignacion = asignacion_actual.copy()

                nueva_asignacion[siguiente_llanta] = empresa

                nuevas_usadas = empresas_usadas.copy()

                nuevas_usadas.append(empresa)

                nuevo_estado = {
                    "asignacion": nueva_asignacion,
                    "usadas": nuevas_usadas
                }

                hijo = Nodo(nuevo_estado)

                hijo.set_padre(nodo_actual)

                nuevo_costo = (
                    nodo_actual.get_costo()
                    + costos_base[empresa][siguiente_llanta]
                )

                hijo.set_costo(nuevo_costo)

                lista_hijos.append(hijo)

                nodos_frontera.append(hijo)

        nodo_actual.set_hijos(lista_hijos)

    return None


# ------------------------------------------
# MOSTRAR RESULTADO
# ------------------------------------------

if __name__ == "__main__":

    solucion = buscar_solucion_Aestrella()

    if solucion is not None:

        resultado = solucion.get_datos()["asignacion"]

        print("================================")
        print("MEJOR SOLUCION ENCONTRADA")
        print("================================")

        for llanta in resultado:

            print(
                "Llanta",
                llanta,
                "->",
                resultado[llanta]
            )

        print("\nCosto minimo total:", solucion.get_costo())

    else:
        print("No se encontró solución")