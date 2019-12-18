function eliminarEntrada(idEntrada, modo)
{

    $("#confirm-modal").modal('show')
    let borrar = document.getElementById('modal_borrar');
    borrar.href = "/inventario/eliminar/" + modo + "/" + idEntrada

} 