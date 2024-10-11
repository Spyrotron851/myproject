from .models import ContadorNotificaciones, Carrito

# Variable para almacenar los mensajes anteriores

def limpiar_mensajes_antiguos(mensajes_anteriores, limite=10):
    """
    Limpia la lista de mensajes anteriores, manteniendo un número máximo de mensajes (limite).
    """
    if len(mensajes_anteriores) > limite:
        mensajes_anteriores = mensajes_anteriores[-limite:]
    return mensajes_anteriores


def contadorymensajes_context(request):
    # Obtener el contador de notificaciones del carrito del usuario
    if request.user.is_authenticated:
        carrito_usuario, created = Carrito.objects.get_or_create(usuario=request.user)
        contador_notificaciones = carrito_usuario.contador_notificaciones
    else:
        contador_notificaciones = None

    # Obtener el último mensaje antes de renderizar el template
    mensaje_actual = ""
    if contador_notificaciones:
        mensaje_actual = contador_notificaciones.mensaje

    # Obtener la lista de mensajes anteriores de la sesión o crear una lista vacía
    mensajes_anteriores = request.session.get('mensajes_anteriores', [])

    # Limpiar mensajes antiguos (mantener los últimos 10)
    mensajes_anteriores = limpiar_mensajes_antiguos(mensajes_anteriores, limite=10)

    # Verificar si el mensaje actual es diferente al último mensaje agregado
    if mensaje_actual != mensajes_anteriores[-1] if mensajes_anteriores else "":
        # Agregar el mensaje actual a la lista de mensajes anteriores
        mensajes_anteriores.append(mensaje_actual)
        request.session['mensajes_anteriores'] = mensajes_anteriores

    # Agregar las variables necesarias al contexto
    variables_contexto = {
        'contador_notificaciones': contador_notificaciones,
        'mensaje_actual': mensaje_actual,
        'mensajes_anteriores': mensajes_anteriores,
    }

    return variables_contexto