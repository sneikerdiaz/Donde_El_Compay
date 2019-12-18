#----------------------------FUNCIONES DE AYUDA Y COMPLEMENTO--------------------------------------------------

from .models import Producto, Opciones
from decimal import Decimal


def obtenerIdProducto(descripcion):
    id_producto = Producto.objects.get(descripcion=descripcion)
    resultado = id_producto.id

    return resultado

def productoTieneIva(idProducto):
    iva = Producto.objects.get(id=idProducto)
    resultado = iva.tiene_iva
    
    return resultado

def sacarIva(elemento):
    iva = Opciones.objects.get(id=1)
    ivaSacado =  iva.valor_iva/100
    resultado = elemento + (elemento * Decimal(ivaSacado))  
    return resultado    

def ivaActual(modo):
    if modo == 'valor':
        iva = Opciones.objects.get(id=1)    
        return iva.valor_iva

    elif modo == 'objeto':
        iva = Opciones.objects.get(id=1)    
        return iva

def obtenerProducto(idProducto):
    producto = Producto.objects.get(id=idProducto)      
    return producto


def complementarContexto(contexto,datos):
    contexto['usuario'] = datos.username
    contexto['id_usuario'] = datos.id
    contexto['nombre'] = datos.first_name
    contexto['apellido'] = datos.last_name
    contexto['correo'] = datos.email

    return contexto

def usuarioExiste(Usuario,buscar,valor):
    if buscar == 'username':
        try:
            Usuario.objects.get(username=valor)
            return True
        except Usuario.DoesNotExist:
            return False

    elif buscar == 'email':
        try:
            Usuario.objects.get(email=valor)
            return True
        except Usuario.DoesNotExist:
            return False

def manejarArchivo(archivo,ruta):
    with open(ruta, 'wb+') as destino:
        for chunk in archivo.chunks():
            destino.write(chunk)


def render_to_pdf(template_src, context_dict={}):
    import io
    from xhtml2pdf import pisa
    from django.template.loader import get_template
    from django.http import HttpResponse

    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None  

#--------------------------------------------------------------------------------------------------------------                 

