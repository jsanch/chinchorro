function NuevoAjax() {
    var xmlhttp = false;
    try {
        xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
    } catch (e) {
        try {
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        } catch (E) {
            xmlhttp = false;
        }
    }

    if (!xmlhttp && typeof XMLHttpRequest != 'undefined') {
        xmlhttp = new XMLHttpRequest();
    }
    return xmlhttp;
}

function cargar_pagina(url, contenedor) {
    ajax = NuevoAjax();
    ajax.open("GET", url, true);
    ajax.onreadystatechange = function() {
        if (ajax.readyState == 1) {
            //Sucede cuando se esta cargando la pagina
            contenedor.innerHTML = "<img border='0' src='../Estilo/img/loading.gif' />";
        } else if (ajax.readyState == 4) {
            //Sucede cuando la pagina se cargó
            if (ajax.status == 200) {
                //Todo OK
                document.getElementById(contenedor).innerHTML = ajax.responseText;
            } else if (ajax.status == 404) {
            //La pagina no existe
                document.getElementById(contenedor).innerHTML = "La página no existe";
            } else {
                //Mostramos el posible error
                document.getElementById(contenedor).innerHTML = "Error:".ajax.status;
            }
        }
    }
    ajax.send(null);
}