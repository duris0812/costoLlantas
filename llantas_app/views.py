from django.shortcuts import redirect, render

from algortimo_llantas import costos as costos_defecto, buscar_solucion_Aestrella, tipos_llantas


def construir_tabla_costos(costos_base):
    proveedores = list(costos_base.keys())
    filas = []
    for llanta in tipos_llantas:
        fila = {
            'llanta': llanta,
            'valores': [costos_base[proveedor][llanta] for proveedor in proveedores],
        }
        filas.append(fila)
    return proveedores, filas


def obtener_costos_actuales(request):
    return request.session.get('costos_personalizados', costos_defecto)


def construir_matriz_edicion(costos_base):
    matriz = []
    for proveedor, valores in costos_base.items():
        fila = {
            'proveedor': proveedor,
            'celdas': [
                {
                    'llanta': llanta,
                    'valor': valores[llanta],
                }
                for llanta in tipos_llantas
            ],
        }
        matriz.append(fila)
    return matriz


def preparar_costos_desde_post(request, costos_base):
    nuevos_costos = {}
    for proveedor in costos_base:
        nuevos_costos[proveedor] = {}
        for llanta in tipos_llantas:
            campo = f'costo_{proveedor}_{llanta}'
            valor = request.POST.get(campo, '').strip()
            if valor == '':
                valor = costos_base[proveedor][llanta]
            nuevos_costos[proveedor][llanta] = int(valor)
    return nuevos_costos


def guardar_costos_en_sesion(request, nuevos_costos):
    request.session['costos_personalizados'] = nuevos_costos


def guardar_resultado_en_sesion(request, resultado):
    request.session['mejor_solucion'] = resultado


def obtener_resultado_guardado(request):
    return request.session.get('mejor_solucion')


def guardar_mensaje(request, texto, tipo='info'):
    request.session['flash_message'] = texto
    request.session['flash_type'] = tipo


def obtener_mensaje_flash(request):
    mensaje = request.session.pop('flash_message', None)
    tipo = request.session.pop('flash_type', None)
    return mensaje, tipo


def construir_mejor_solucion(costos_base):
    solucion = buscar_solucion_Aestrella(costos_base)
    if solucion is None:
        return None

    asignacion = solucion.get_datos()['asignacion']
    filas = []
    total = 0

    for llanta in tipos_llantas:
        proveedor = asignacion[llanta]
        costo = costos_base[proveedor][llanta]
        total += costo
        filas.append({
            'llanta': llanta,
            'proveedor': proveedor,
            'costo': costo,
        })

    return {
        'filas': filas,
        'total': total,
    }


def index(request):
    costos_base = obtener_costos_actuales(request)
    mensaje, mensaje_tipo = obtener_mensaje_flash(request)
    modo_edicion = request.GET.get('editar') == '1'
    mejor_solucion = obtener_resultado_guardado(request)

    if request.method == 'POST':
        accion = request.POST.get('action')
        if accion == 'guardar_costos' or accion == 'buscar_solucion':
            try:
                costos_base = preparar_costos_desde_post(request, costos_base)
                guardar_costos_en_sesion(request, costos_base)
            except ValueError:
                guardar_mensaje(request, 'Todos los costos deben ser números enteros.', 'error')
                return redirect(request.path)

        if accion == 'guardar_costos':
            request.session.pop('mejor_solucion', None)
            guardar_mensaje(request, 'Tabla actualizada correctamente.', 'success')
            return redirect(request.path)

        if accion == 'buscar_solucion':
            mejor_solucion = construir_mejor_solucion(costos_base)
            guardar_resultado_en_sesion(request, mejor_solucion)
            if mejor_solucion is None:
                guardar_mensaje(request, 'No se encontró una solución válida.', 'error')
            else:
                guardar_mensaje(request, 'Mejor solución calculada correctamente.', 'success')
            return redirect(request.path)

    proveedores, tabla_costos = construir_tabla_costos(costos_base)
    matriz_edicion = construir_matriz_edicion(costos_base)

    contexto = {
        'proveedores': proveedores,
        'tabla_costos': tabla_costos,
        'matriz_edicion': matriz_edicion,
        'mejor_solucion': mejor_solucion,
        'mensaje': mensaje,
        'mensaje_tipo': mensaje_tipo,
        'modo_edicion': modo_edicion,
        'tipos_llantas': tipos_llantas,
    }
    return render(request, 'llantas_app/index.html', contexto)
