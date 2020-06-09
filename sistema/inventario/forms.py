from django import forms
from .models import Producto,Cliente, Proveedor, Usuario, Opciones

from django.forms import ModelChoiceField

class MisProductos(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.descripcion

class MisPrecios(ModelChoiceField):
    def label_from_instance(self,obj):
        return "%s" % obj.precio

class MisDisponibles(ModelChoiceField):
    def label_from_instance(self,obj):
        return "%s" % obj.disponible


class LoginFormulario(forms.Form):
    username = forms.CharField(label="Tu nombre de usuario",widget=forms.TextInput(attrs={'placeholder': 'Tu nombre de usuario',
        'class': 'form-control underlined', 'type':'text','id':'user'}))

    password = forms.CharField(label="Contraseña",widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña',
        'class': 'form-control underlined', 'type':'password','id':'password'}))

class ProductoFormulario(forms.ModelForm):
    precio = forms.DecimalField(
        min_value = 0,
        label = 'Precio',
        widget = forms.NumberInput(
        attrs={'placeholder': 'Precio del producto',
        'id':'precio','class':'form-control'}),
        )
    class Meta:
        model = Producto
        fields = ['descripcion','precio','categoria','tiene_iva']
        labels = {
        'descripcion': 'Nombre',
        'tiene_iva': 'Incluye IVA?'
        }
        widgets = {
        'descripcion': forms.TextInput(attrs={'placeholder': 'Nombre del producto',
        'id':'descripcion','class':'form-control'} ),
        'categoria': forms.Select(attrs={'class':'form-control','id':'categoria'}),
        'tiene_iva': forms.CheckboxInput(attrs={'class':'checkbox rounded','id':'tiene_iva'}) 
        }

class ImportarProductosFormulario(forms.Form):
    importar = forms.FileField(
        max_length = 100000000000,
        label = 'Escoger archivo',
        widget = forms.ClearableFileInput(
        attrs={'id':'importar','class':'form-control'}),
        )

class ImportarClientesFormulario(forms.Form):
    importar = forms.FileField(
        max_length = 100000000000,
        label = 'Escoger archivo',
        widget = forms.ClearableFileInput(
        attrs={'id':'importar','class':'form-control'}),
        )   

class ExportarProductosFormulario(forms.Form):
    desde = forms.DateField(
        label = 'Desde',
        widget = forms.DateInput(format=('%d-%m-%Y'),
        attrs={'id':'desde','class':'form-control','type':'date'}),
        )   

    hasta = forms.DateField(
        label = 'Hasta',
        widget = forms.DateInput(format=('%d-%m-%Y'),
        attrs={'id':'hasta','class':'form-control','type':'date'}),
        )   

class ExportarClientesFormulario(forms.Form):
    desde = forms.DateField(
        label = 'Desde',
        widget = forms.DateInput(format=('%d-%m-%Y'),
        attrs={'id':'desde','class':'form-control','type':'date'}),
        )   

    hasta = forms.DateField(
        label = 'Hasta',
        widget = forms.DateInput(format=('%d-%m-%Y'),
        attrs={'id':'hasta','class':'form-control','type':'date'}),
        )   


class ClienteFormulario(forms.ModelForm):
    tipoC =  [ ('1','V'),('2','E') ]

    telefono2 = forms.CharField(
        required = False,
        label = 'Segundo numero telefonico',
        widget = forms.TextInput(
        attrs={'placeholder': 'Inserte el telefono alternativo del cliente',
        'id':'telefono2','class':'form-control'}),
        )

    correo2 = forms.CharField(
        required=False,
        label = 'Segundo correo electronico',
        widget = forms.TextInput(
        attrs={'placeholder': 'Inserte el correo alternativo del cliente',
        'id':'correo2','class':'form-control'}),
        )

    tipoCedula = forms.CharField(
        label="Tipo de cedula",
        max_length=2,
        widget=forms.Select(choices=tipoC,attrs={'placeholder': 'Tipo de cedula',
        'id':'tipoCedula','class':'form-control'}
        )
        )


    class Meta:
        model = Cliente
        fields = ['tipoCedula','cedula','nombre','apellido','direccion','nacimiento','telefono','correo','telefono2','correo2']
        labels = {
        'cedula': 'Cedula del cliente',
        'nombre': 'Nombre del cliente',
        'apellido': 'Apellido del cliente',
        'direccion': 'Direccion del cliente',
        'nacimiento': 'Fecha de nacimiento del cliente',
        'telefono': 'Numero telefonico del cliente',
        'correo': 'Correo electronico del cliente',
        'telefono2': 'Segundo numero telefonico',
        'correo2': 'Segundo correo electronico'
        }
        widgets = {
        'cedula': forms.TextInput(attrs={'placeholder': 'Inserte la cedula de identidad del cliente',
        'id':'cedula','class':'form-control'} ),
        'nombre': forms.TextInput(attrs={'placeholder': 'Inserte el primer o primeros nombres del cliente',
        'id':'nombre','class':'form-control'}),
        'apellido': forms.TextInput(attrs={'class':'form-control','id':'apellido','placeholder':'El apellido del cliente'}),
        'direccion': forms.TextInput(attrs={'class':'form-control','id':'direccion','placeholder':'Direccion del cliente'}), 
        'nacimiento':forms.DateInput(format=('%d-%m-%Y'),attrs={'id':'hasta','class':'form-control','type':'date'} ),
        'telefono':forms.TextInput(attrs={'id':'telefono','class':'form-control',
        'placeholder':'El telefono del cliente'} ),
        'correo':forms.TextInput(attrs={'placeholder': 'Correo del cliente',
        'id':'correo','class':'form-control'} )
        }


class EmitirFacturaFormulario(forms.Form):
    def __init__(self, *args, **kwargs):
       elecciones = kwargs.pop('cedulas')
       super(EmitirFacturaFormulario, self).__init__(*args, **kwargs)

       if(elecciones):
            self.fields["cliente"] = forms.CharField(label="Cliente a facturar",max_length=50,
            widget=forms.Select(choices=elecciones,
            attrs={'placeholder': 'La cedula del cliente a facturar',
            'id':'cliente','class':'form-control'}))
    
    productos = forms.IntegerField(label="Numero de productos",widget=forms.NumberInput(attrs={'placeholder': 'Numero de productos a facturar',
        'id':'productos','class':'form-control'}))

class DetallesFacturaFormulario(forms.Form):
    productos = Producto.productosRegistrados()

    descripcion = MisProductos(queryset=productos,widget=forms.Select(attrs={'placeholder': 'El producto a debitar','class':'form-control select-group','onchange':'establecerOperaciones(this)'}))

    vista_precio = MisPrecios(required=False,queryset=productos,label="Precio del producto",widget=forms.Select(attrs={'placeholder': 'El precio del producto','class':'form-control','disabled':'true'}))

    cantidad = forms.IntegerField(label="Cantidad a facturar",min_value=0,widget=forms.NumberInput(attrs={'placeholder': 'Introduzca la cantidad del producto','class':'form-control','value':'0','onchange':'calculoPrecio(this);calculoDisponible(this)', 'max':'0'}))

    cantidad_disponibles = forms.IntegerField(required=False,label="Stock disponible",min_value=0,widget=forms.NumberInput(attrs={'placeholder': 'Introduzca la cantidad del producto','class':'form-control','value':'0', 'max':'0', 'disabled':'true'}))

    selec_disponibles = MisDisponibles(queryset=productos,required=False,widget=forms.Select(attrs={'placeholder': 'El producto a debitar','class':'form-control','disabled':'true','hidden':'true'}))

    subtotal = forms.DecimalField(required=False,label="Sub-total",min_value=0,widget=forms.NumberInput(attrs={'placeholder': 'Monto sub-total','class':'form-control','disabled':'true','value':'0'}))

    valor_subtotal = forms.DecimalField(min_value=0,widget=forms.NumberInput(attrs={'placeholder': 'Monto sub-total','class':'form-control','hidden':'true','value':'0'}))      


class EmitirPedidoFormulario(forms.Form):
    def __init__(self, *args, **kwargs):
       elecciones = kwargs.pop('cedulas')
       super(EmitirPedidoFormulario, self).__init__(*args, **kwargs)

       if(elecciones):
            self.fields["proveedor"] = forms.CharField(label="Proveedor",max_length=50,
            widget=forms.Select(choices=elecciones,attrs={'placeholder': 'La cedula del proveedor que vende el producto',
            'id':'proveedor','class':'form-control'}))

    productos = forms.IntegerField(label="Numero de productos",widget=forms.NumberInput(attrs={'placeholder': 'Numero de productos a comprar',
        'id':'productos','class':'form-control'}))


class DetallesPedidoFormulario(forms.Form):
    productos = Producto.productosRegistrados()
    precios = Producto.preciosProductos()

    descripcion = MisProductos(queryset=productos,widget=forms.Select(attrs={'placeholder': 'El producto a debitar','class':'form-control','onchange':'establecerPrecio(this)'}))

    vista_precio = MisPrecios(required=False,queryset=productos,label="Precio del producto",widget=forms.Select(attrs={'placeholder': 'El precio del producto','class':'form-control','disabled':'true'}))

    cantidad = forms.IntegerField(label="Cantidad",min_value=0,widget=forms.NumberInput(attrs={'placeholder': 'Introduzca la cantidad del producto','class':'form-control','value':'0','onchange':'calculoPrecio(this)'}))

    subtotal = forms.DecimalField(required=False,label="Sub-total",min_value=0,widget=forms.NumberInput(attrs={'placeholder': 'Monto sub-total','class':'form-control','disabled':'true','value':'0'}))

    valor_subtotal = forms.DecimalField(min_value=0,widget=forms.NumberInput(attrs={'placeholder': 'Monto sub-total','class':'form-control','hidden':'true','value':'0'}))      




class ProveedorFormulario(forms.ModelForm):
    tipoC =  [ ('1','V'),('2','E') ]

    telefono2 = forms.CharField(
        required = False,
        label = 'Segundo numero telefonico( Opcional )',
        widget = forms.TextInput(
        attrs={'placeholder': 'Inserte el telefono alternativo del proveedor',
        'id':'telefono2','class':'form-control'}),
        )

    correo2 = forms.CharField(
        required=False,
        label = 'Segundo correo electronico( Opcional )',
        widget = forms.TextInput(
        attrs={'placeholder': 'Inserte el correo alternativo del proveedor',
        'id':'correo2','class':'form-control'}),
        )

    tipoCedula = forms.CharField(
        label="Tipo de cedula",
        max_length=2,
        widget=forms.Select(choices=tipoC,attrs={'placeholder': 'Tipo de cedula',
        'id':'tipoCedula','class':'form-control'}
        )
        )


    class Meta:
        model = Cliente
        fields = ['tipoCedula','cedula','nombre','apellido','direccion','nacimiento','telefono','correo','telefono2','correo2']
        labels = {
        'cedula': 'Cedula del proveedor',
        'nombre': 'Nombre del proveedor',
        'apellido': 'Apellido del proveedor',
        'direccion': 'Direccion del proveedor',
        'nacimiento': 'Fecha de nacimiento del proveedor',
        'telefono': 'Numero telefonico del proveedor',
        'correo': 'Correo electronico del proveedor',
        'telefono2': 'Segundo numero telefonico',
        'correo2': 'Segundo correo electronico'
        }
        widgets = {
        'cedula': forms.TextInput(attrs={'placeholder': 'Inserte la cedula de identidad del proveedor',
        'id':'cedula','class':'form-control'} ),
        'nombre': forms.TextInput(attrs={'placeholder': 'Inserte el primer o primeros nombres del proveedor',
        'id':'nombre','class':'form-control'}),
        'apellido': forms.TextInput(attrs={'class':'form-control','id':'apellido','placeholder':'El apellido del proveedor'}),
        'direccion': forms.TextInput(attrs={'class':'form-control','id':'direccion','placeholder':'Direccion del proveedor'}), 
        'nacimiento':forms.DateInput(format=('%d-%m-%Y'),attrs={'id':'hasta','class':'form-control','type':'date'} ),
        'telefono':forms.TextInput(attrs={'id':'telefono','class':'form-control',
        'placeholder':'El telefono del proveedor'} ),
        'correo':forms.TextInput(attrs={'placeholder': 'Correo del proveedor',
        'id':'correo','class':'form-control'} )
        } 


class UsuarioFormulario(forms.Form):
    niveles =  [ ('1','Administrador'),('0','Usuario') ]

    username = forms.CharField(
        label = "Nombre de usuario",
        max_length=50,
        widget = forms.TextInput(attrs={'placeholder': 'Inserte un nombre de usuario',
        'id':'username','class':'form-control','value':''} ),
        )

    first_name = forms.CharField(
        label = 'Nombre',
        max_length =100,
        widget = forms.TextInput(attrs={'placeholder': 'Inserte un nombre',
        'id':'first_name','class':'form-control','value':''}),            
        )

    last_name = forms.CharField(
        label = 'Apellido',
        max_length = 100,
        widget = forms.TextInput(attrs={'class':'form-control','id':'last_name','placeholder':'Inserte un apellido','value':''}), 
        )

    email = forms.CharField(
        label = 'Correo electronico',
        max_length=100,
        widget = forms.TextInput(attrs={'placeholder': 'Inserte un correo valido',
        'id':'email','class':'form-control','type':'email','value':''} )
        )

    level =  forms.CharField(
        required=False,
        label="Nivel de acceso",
        max_length=2,
        widget=forms.Select(choices=niveles,attrs={'placeholder': 'El nivel de acceso',
        'id':'level','class':'form-control','value':''}
        )
        )

class NuevoUsuarioFormulario(forms.Form):
    niveles =  [ ('1','Administrador'),('0','Usuario') ]

    username = forms.CharField(
        label = "Nombre de usuario",
        max_length=50,
        widget = forms.TextInput(attrs={'placeholder': 'Inserte un nombre de usuario',
        'id':'username','class':'form-control','value':''} ),
        )

    first_name = forms.CharField(
        label = 'Nombre',
        max_length =100,
        widget = forms.TextInput(attrs={'placeholder': 'Inserte un nombre',
        'id':'first_name','class':'form-control','value':''}),            
        )

    last_name = forms.CharField(
        label = 'Apellido',
        max_length = 100,
        widget = forms.TextInput(attrs={'class':'form-control','id':'last_name','placeholder':'Inserte un apellido','value':''}), 
        )

    email = forms.CharField(
        label = 'Correo electronico',
        max_length=100,
        widget = forms.TextInput(attrs={'placeholder': 'Inserte un correo valido',
        'id':'email','class':'form-control','type':'email','value':''} )
        )    

    password = forms.CharField(
        label = 'Clave',
        max_length=100,
        widget = forms.TextInput(attrs={'placeholder': 'Inserte una clave',
        'id':'password','class':'form-control','type':'password','value':''} )
        )  

    rep_password = forms.CharField(
        label = 'Repetir clave',
        max_length=100,
        widget = forms.TextInput(attrs={'placeholder': 'Repita la clave de arriba',
        'id':'rep_password','class':'form-control','type':'password','value':''} )
        )  

    level =  forms.CharField(
        label="Nivel de acceso",
        max_length=2,
        widget=forms.Select(choices=niveles,attrs={'placeholder': 'El nivel de acceso',
        'id':'level','class':'form-control','value':''}
        )
        )


class ClaveFormulario(forms.Form):
    #clave = forms.CharField(
        #label = 'Ingrese su clave actual',
        #max_length=50,
        #widget = forms.TextInput(
        #attrs={'placeholder': 'Inserte la clave actual para verificar su identidad',
        #'id':'clave','class':'form-control', 'type': 'password'}),
        #)

    clave_nueva = forms.CharField(
        label = 'Ingrese la clave nueva',
        max_length=50,
        widget = forms.TextInput(
        attrs={'placeholder': 'Inserte la clave nueva de acceso',
        'id':'clave_nueva','class':'form-control', 'type': 'password'}),
        )

    repetir_clave = forms.CharField(
        label="Repita la clave nueva",
        max_length=50,
        widget = forms.TextInput(
        attrs={'placeholder': 'Vuelva a insertar la clave nueva',
        'id':'repetir_clave','class':'form-control', 'type': 'password'}),
        )


class ImportarBDDFormulario(forms.Form):
    archivo = forms.FileField(
        widget=forms.FileInput(
            attrs={'placeholder': 'Archivo de la base de datos',
            'id':'customFile','class':'custom-file-input'})
        )

class OpcionesFormulario(forms.Form):
    moneda = forms.CharField(
        label = 'Moneda a emplear en el sistema',
        max_length=20,
        widget = forms.TextInput(
        attrs={'placeholder': 'Inserte la abreviatura de la moneda que quiere usar (Ejemplo: $)',
        'id':'moneda','class':'form-control'}),
        )

    valor_iva = forms.DecimalField(
        label="Valor del IVA",
        min_value=0,widget=forms.NumberInput(
            attrs={'placeholder': 'Introduzca el IVA actual',
            'class':'form-control','id':'valor_iva'}))

    mensaje_factura = forms.CharField(
        label = 'Mensaje personal que va en las facturas',
        max_length=50,
        widget = forms.TextInput(
        attrs={'placeholder': 'Inserte el mensaje personal que ira en el pie de la factura',
        'id':'mensaje_factura','class':'form-control'}),
        )

    nombre_negocio = forms.CharField(
        label = 'Nombre actual del negocio',
        max_length=50,
        widget = forms.TextInput(
        attrs={'class':'form-control','id':'nombre_negocio',
            'placeholder':'Coloque el nombre actual del negocio'}),
        )

    imagen = forms.FileField(required=False,widget = forms.FileInput(
        attrs={'class':'custom-file-input','id':'customFile'}))
