//se obtiene el numero de productos a facturar
let productos = document.getElementById('id_form-TOTAL_FORMS').value 

idCalculoDisponible = "";


// se utiliza en calculoDisponible, pero se resetea en establecerDisponibles
let ultimoValor = 0

//se utiliza en calculoDisponible
let usado = 0 

/*matriz que guarda que productos se han seleccionado en cada formulario. se inicia en 
arreglosProductos
*/
let productosUsados = [] 

/* matriz que guarda los productos anteriores */
let productosAnteriores = []

/* se usa como variable temporal en establecerUsados */
let valorAnterior = null

let indiceABorrar = null


const selects = document.querySelectorAll('.select-group');
selects.forEach( (elem) => {
	elem.addEventListener('change',(event) => {
		let values = Array.from(selects).map(select => select.value);
		for(let select of selects)
		{
			select.querySelectorAll('option').forEach((option) => {
			let value = option.value;
			if(value && value !== select.value && values.includes(value)) {
				option.disabled = true;
			} else {
				option.disabled = false;
			}
			});
		}
	});
});


window.onload
{
	inicializarCampos(1)

}



function establecerOperaciones(elemento)
{
	establecerPrecio(elemento)
	establecerDisponibles(elemento)

}

function idNuevo(nombreViejo,separador,posicion,cambio)
{
	let nombreTemporal = nombreViejo.split(separador) // nombre temporal de la id del campo cantidad en forma de array

 	nombreTemporal[posicion] = cambio // se le cambia el segmento a la parte que se desea enlazar

	let nuevoNombre = nombreTemporal.join(separador) //se convierte el array a un string para ser procesado
	// hasta aqui esta bien jejejejej

 	return nuevoNombre
}


function deStringANumero(numero)
{
	return parseInt(numero,10)
}	


function inicializarCampos(primeraVez)
{

for(let i = 0; i < productos; i++) //el bucle que recorre cada campo de descripcion de cada producto
{
	let descripcion = document.getElementById('id_form-'+i+'-descripcion')//una variable que guarda cada campo


	if(primeraVez == 1)
	{
		descripcion.selectedIndex = 0
		let precio = document.getElementById('id_form-'+i+'-vista_precio')
		let subtotal = document.getElementById('id_form-'+i+'-subtotal')
		let disponibles = document.getElementById('id_form-'+i+'-selec_disponibles')
		let cantidadDisponibles = document.getElementById('id_form-'+i+'-cantidad_disponibles')

		precio.selectedIndex = 0
		subtotal.value = 0
		subtotal.selectedIndex = 0
		disponibles.selectedIndex = 0
		cantidadDisponibles.value = 0
	}

	if(descripcion.selectedIndex == 0) //si el indice de el campo actual es cero.....
	{

		let cantidad = document.getElementById('id_form-'+i+'-cantidad')
		cantidad.value = 0
		cantidad.disabled = true 
	}

	else
	{
		let cantidad = document.getElementById('id_form-'+i+'-cantidad')
		cantidad.disabled = false

	}
}

}





function clienteCamposOcultos(esto)
{
	let check = esto.checked

	let segTelefono = document.getElementById('div_telefono2')
	let segCorreo = document.getElementById('div_correo2')



	if(check)
	{

		$(document).ready(function(){
		segTelefono.hidden = '';
		segCorreo.hidden = '';
									}
									)
	}

	else
	{
		$(document).ready(function(){
		segTelefono.hidden = 'true';
		segCorreo.hidden = 'true';
									}
									)
	}

	}


function calculoPrecio(elemento)
{
	let idCantidad = elemento.id //la id del campo de cantidad

	let valorCantidad = elemento.value // el valor actual del campo cantidad

	let precioNuevo = idNuevo(idCantidad,'-',2,'vista_precio') // campo de precio

 	let subTotalNuevo = idNuevo(idCantidad,'-',2,'subtotal') //el campo que visualiza el subtotal

 	let valorSubTotal = idNuevo(idCantidad,'-',2,'valor_subtotal')

	let precio = document.getElementById(precioNuevo)

	let elementoAModificar = document.getElementById(subTotalNuevo)

	elementoAModificar.value = valorCantidad * precio.item(precio.selectedIndex).text

	let valorSub = document.getElementById(valorSubTotal)

	valorSub.value = elementoAModificar.value

}


function calculoDisponible(elemento)
{
	//obtengo el select por la id de arriba
	let idDisponible = document.getElementById(idNuevo(elemento.id,'-',2,'selec_disponibles')) 

	//el number input
	let cantidadIdDisponible = document.getElementById(idNuevo(elemento.id,'-',2,'cantidad_disponibles')) 

	let nuevoValor = 0


	if(elemento.value == elemento.defaultValue)
	{

		if(usado != 0)
		{
			nuevoValor = deStringANumero(cantidadIdDisponible.value) + 1
			cantidadIdDisponible.value = nuevoValor
		}

		else
		{
			ultimoValor = elemento.value
		}

	}

	else
	{
		if(deStringANumero(elemento.value) < deStringANumero(ultimoValor) )
		{
			nuevoValor = deStringANumero(cantidadIdDisponible.value) + 1
			usado = 1
		}

		else
		{
			nuevoValor = deStringANumero(cantidadIdDisponible.value) - 1
			usado = 1
		}

		ultimoValor = elemento.value
	}

	cantidadIdDisponible.value = nuevoValor	


}

function establecerDisponibles(elemento)
{

	inicializarCampos(0)

	ultimoValor = 0

	let nombre = elemento.id
	let lista = document.getElementById(elemento.id)
	let idProducto = lista.value

	let elementoAModificar = document.getElementById(idNuevo(nombre,'-',2,'selec_disponibles'))
	let cantidadFacturar = document.getElementById( idNuevo(nombre,'-',2,'cantidad') )

	cantidadFacturar.value = 0

	let seguir = true

	for(let i = 0; i < lista.children.length; i++)
	{
		if(idProducto == elementoAModificar[i].value && seguir)
		{
			elementoAModificar.selectedIndex = i
			seguir = false
		}
	}

	let maximo = elementoAModificar[elementoAModificar.selectedIndex].text
	cantidadFacturar.max = maximo


	let stockDisponible = document.getElementById(idNuevo(nombre,'-',2,'cantidad_disponibles'))
	stockDisponible.value = maximo
	stockDisponible.max = maximo


}

function establecerPrecio(elemento)
{
	inicializarCampos(0)

	let nombre = elemento.id
	let lista = document.getElementById(elemento.id)
	let idProducto = lista.value

	let nombreNuevo = idNuevo(nombre,'-',2,'vista_precio')

	let elementoAModificar = document.getElementById(nombreNuevo)
	let seguir = true

	for(let i = 0; i < lista.children.length; i++)
	{
		if(idProducto == elementoAModificar[i].value && seguir)
		{
			elementoAModificar.selectedIndex = i
			seguir = false
		}
	}

}






