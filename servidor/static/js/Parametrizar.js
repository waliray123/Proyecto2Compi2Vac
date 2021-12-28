function Parametrizar() {
    let valorAnalisis = document.getElementById("inputGroupSelect01").value;
    if (valorAnalisis == 0) {
        alert("Debe escoger algun tipo de analisis");
    } else {
        let valR = obtenerValorHTMLIns(valorAnalisis);
        let divParametrizar = document.getElementById("Parametros");
        divParametrizar.innerHTML = valR;
    }
}

function obtenerValorHTMLIns(valorAnalisis) {
    let strRet = '';
    strRet += '<h2>Parametrizar y Subir Archivo</h2>\n<form>\n<div>\n<input class="form-control form-control" id="formFileLg" type="file" accept=".xls,.xlsx,.csv,.json">\n</div>\n</form>';

    console.log(valorAnalisis);
    if (valorAnalisis == 1) {        

        strRet += '<div class="form-group"><label for="nombrePais">Nombre del Pais</label><input type="text" class="form-control" id="nombrePais" placeholder="Guatemala"></div>';
        strRet += '<div class="form-group"><label for="campodia">Campo del dia</label><input type="text" class="form-control" id="campodia" placeholder="dias"></div>';
        strRet += '<div class="form-group"><label for="camponum">Campo No.Casos</label><input type="text" class="form-control" id="camponum" placeholder="casos"></div>';

    }
    strRet += '<br><div class="d-grid gap-2 d-md-flex justify-content-md-end"><button type="submit" class="btn btn-primary">Analizar</button></div>';

    return strRet;
}