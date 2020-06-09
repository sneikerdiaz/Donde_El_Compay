from django.db import models
from django.contrib.auth.models import AbstractUser


# MODELOS

#--------------------------------USUARIO------------------------------------------------
class Usuario(AbstractUser):
    #id
    username = models.CharField(max_length=80, unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=60)
    nivel = models.IntegerField(null=True) 

    @classmethod
    def numeroRegistrados(self):
        return int(self.objects.all().count() )   

    @classmethod
    def numeroUsuarios(self,tipo):
        if tipo == 'administrador':
            return int(self.objects.filter(is_superuser = True).count() )
        elif tipo == 'usuario':
            return int(self.objects.filter(is_superuser = False).count() )


class Opciones(models.Model):
    #id
    moneda = models.CharField(max_length=20, null=True)
    valor_iva = models.IntegerField(unique=True)   
    nombre_negocio = models.CharField(max_length=25,null=True)
    mensaje_factura = models.TextField(null=True)

#---------------------------------------------------------------------------------------

 
#-------------------------------PRODUCTO------------------------------------------------
class Producto(models.Model):
    #id
    decisiones =  [('1','Unidad'),('2','Kilo'),('3','Litro'),('4','Otros')]
    descripcion = models.CharField(max_length=40)
    precio = models.DecimalField(max_digits=9,decimal_places=2)
    disponible = models.IntegerField(null=True)
    categoria = models.CharField(max_length=20,choices=decisiones)
    tiene_iva = models.BooleanField(null=True)

    @classmethod
    def numeroRegistrados(self):
        return int(self.objects.all().count() )
   

    @classmethod
    def productosRegistrados(self):
        objetos = self.objects.all().order_by('descripcion')
        return objetos


    @classmethod
    def preciosProductos(self):
        objetos = self.objects.all().order_by('id')
        arreglo = []
        etiqueta = True
        extra = 1

        for indice,objeto in enumerate(objetos):
            arreglo.append([])
            if etiqueta:
                arreglo[indice].append(0)
                arreglo[indice].append("------")
                etiqueta = False
                arreglo.append([])

            arreglo[indice + extra].append(objeto.id)
            precio_producto = objeto.precio
            arreglo[indice + extra].append("%d" % (precio_producto) )  

        return arreglo 

    @classmethod
    def productosDisponibles(self):
        objetos = self.objects.all().order_by('id')
        arreglo = []
        etiqueta = True
        extra = 1

        for indice,objeto in enumerate(objetos):
            arreglo.append([])
            if etiqueta:
                arreglo[indice].append(0)
                arreglo[indice].append("------")
                etiqueta = False
                arreglo.append([])

            arreglo[indice + extra].append(objeto.id)
            productos_disponibles = objeto.disponible
            arreglo[indice + extra].append("%d" % (productos_disponibles) )  

        return arreglo 
#---------------------------------------------------------------------------------------


#------------------------------------------CLIENTE--------------------------------------
class Cliente(models.Model):
    #id
    cedula = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    direccion = models.CharField(max_length=200)
    nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    telefono2 = models.CharField(max_length=20,null=True)
    correo = models.CharField(max_length=100)
    correo2 = models.CharField(max_length=100,null=True)

    @classmethod
    def numeroRegistrados(self):
        return int(self.objects.all().count() )

    @classmethod
    def cedulasRegistradas(self):
        objetos = self.objects.all().order_by('nombre')
        arreglo = []
        for indice,objeto in enumerate(objetos):
            arreglo.append([])
            arreglo[indice].append(objeto.cedula)
            nombre_cliente = objeto.nombre + " " + objeto.apellido
            arreglo[indice].append("%s. C.I: %s" % (nombre_cliente,self.formatearCedula(objeto.cedula)) )
 
        return arreglo   


    @staticmethod
    def formatearCedula(cedula):
        return format(int(cedula), ',d')        
#-----------------------------------------------------------------------------------------        



#-------------------------------------FACTURA---------------------------------------------
class Factura(models.Model):
    #id
    cliente = models.ForeignKey(Cliente,to_field='cedula', on_delete=models.CASCADE)
    fecha = models.DateField()
    sub_monto = models.DecimalField(max_digits=20,decimal_places=2)
    monto_general = models.DecimalField(max_digits=20,decimal_places=2)
    iva = models.ForeignKey(Opciones,to_field='valor_iva', on_delete=models.CASCADE)

    @classmethod
    def numeroRegistrados(self):
        return int(self.objects.all().count() )

    @classmethod
    def ingresoTotal(self):
        facturas = self.objects.all()
        total = 0

        for factura in facturas:
            total += factura.monto_general

        return total
#-----------------------------------------------------------------------------------------


#-------------------------------------DETALLES DE FACTURA---------------------------------
class DetalleFactura(models.Model):
    #id
    id_factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    sub_total = models.DecimalField(max_digits=20,decimal_places=2)
    total = models.DecimalField(max_digits=20,decimal_places=2)

    @classmethod
    def productosVendidos(self):
        vendidos = self.objects.all()
        totalVendidos = 0
        for producto in vendidos:
            totalVendidos += producto.cantidad

        return totalVendidos  

    @classmethod
    def ultimasVentas(self):
        objetos = self.objects.all().order_by('-id')[:10]

        return objetos
#---------------------------------------------------------------------------------------


#------------------------------------------PROVEEDOR-----------------------------------
class Proveedor(models.Model):
    #id
    cedula = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    direccion = models.CharField(max_length=200)
    nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    telefono2 = models.CharField(max_length=20,null=True)
    correo = models.CharField(max_length=100)
    correo2 = models.CharField(max_length=100,null=True)

    @classmethod
    def cedulasRegistradas(self):
        objetos = self.objects.all().order_by('nombre')
        arreglo = []
        for indice,objeto in enumerate(objetos):
            arreglo.append([])
            arreglo[indice].append(objeto.cedula)
            nombre_cliente = objeto.nombre + " " + objeto.apellido
            arreglo[indice].append("%s. C.I: %s" % (nombre_cliente,self.formatearCedula(objeto.cedula)) )
 
        return arreglo 

    @staticmethod
    def formatearCedula(cedula):
        return format(int(cedula), ',d')  
#---------------------------------------------------------------------------------------    


#----------------------------------------PEDIDO-----------------------------------------
class Pedido(models.Model):
    #id
    proveedor = models.ForeignKey(Proveedor,to_field='cedula', on_delete=models.CASCADE)    
    fecha = models.DateField()
    sub_monto = models.DecimalField(max_digits=20,decimal_places=2)
    monto_general = models.DecimalField(max_digits=20,decimal_places=2)
    iva = models.ForeignKey(Opciones,to_field='valor_iva', on_delete=models.CASCADE)
    presente = models.BooleanField(null=True)

    @classmethod
    def recibido(self,pedido):
        return self.objects.get(id=pedido).presente

#---------------------------------------------------------------------------------------    


#-------------------------------------DETALLES DE PEDIDO-------------------------------
class DetallePedido(models.Model):
    #id
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    sub_total = models.DecimalField(max_digits=20,decimal_places=2)
    total = models.DecimalField(max_digits=20,decimal_places=2)
#---------------------------------------------------------------------------------------


#------------------------------------NOTIFICACIONES------------------------------------
class Notificaciones(models.Model):
    #id
    autor = models.ForeignKey(Usuario,to_field='username', on_delete=models.CASCADE)
    mensaje = models.TextField()
#---------------------------------------------------------------------------------------    