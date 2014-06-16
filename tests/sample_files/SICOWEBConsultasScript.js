// AJAX =========================================================================================== //
var bandera = 0;
var hfText = "ctl00_contenidoArriba_txtOficinasHidden1";
var idText = "ctl00_contenidoArriba_txtOficinas";

function showPanel() {
    document.getElementById("UpdatePanelPadre").style.display = "inline";
    bandera = 1;
}

function hidePanel() {
    if (document.getElementById("UpdatePanelPadre")) {
        if (bandera == 0) {
            document.getElementById("UpdatePanelPadre").style.display = "none";            
        }
        bandera = 0;
    }
}

function buscarCatalogoDeOficinas(idTextbox, idPanel) {
    idText = idTextbox;
    buscar = document.getElementById(idText).value;
    url = "AJAX.aspx";

    if (buscar.length >= 3) {
        text = "?busqueda=" + buscar;
        url += text;
        cargar_pagina(url, idPanel);
    }
    else if (buscar.length == 0) {
        cargar_pagina(url, idPanel);
    }
}

function enviaSeleccionado(idseleccion, nombre) {
    document.getElementById(hfText).value = idseleccion;
    document.getElementById(idText).value = nombre;
    hidePanel();
}

function enviaSeleccionadoOption(idseleccion) {
    document.getElementById("documentoHidden").value = idseleccion;
}