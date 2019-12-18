// Cerrar menú
var j = false;

function abrir() {
    var x = document.getElementById('contenido');
    if(j) {
        x.classList.remove('abrir');
        j = false;
    } else {
        x.classList.add('abrir');
        j = true;
    }
}

// Tabulador abierto por defecto
document.getElementById("defaultOpen").click();

// Función para abrir el contenido de las tabulaciones
function openCity(evt, Name) {
    var i, tabcontent, tablinks;

    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }


    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }


    document.getElementById(Name).style.display = "block";
    evt.currentTarget.className += " active";
}

// Código para abrir y cerrar los acordeones

var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].onclick = function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight){
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    } 
  }
}
