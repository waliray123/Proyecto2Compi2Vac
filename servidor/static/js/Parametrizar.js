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
    strRet += '<h2>Parametrizar y Subir Archivo Excel</h2>\n';
    strRet += '<input id="tipoAnalisis" name="tipoAnalisis" type="hidden" value="'+valorAnalisis+'">\n';
    strRet += '<div class="mb-3">\n<label for="archivoEn" class="form-label">Archivo Entrada</label>\n<input class="form-control" type="file" id="archivoEn" name="archivoEn" accept=".xls,.csv,.json,.xlsx">\n</div>';
    
    if (valorAnalisis == 1 || valorAnalisis == 2) {        
        strRet += '<div class="form-group"><label for="campoPaises">Campo de Paises</label><input type="text" class="form-control" id="campoPaises" name="campoPaises" placeholder="Guatemala" required></div>';
        strRet += '<div class="form-group"><label for="nombrePais">Nombre del Pais</label><input type="text" class="form-control" id="nombrePais" name="nombrePais" placeholder="Guatemala" required></div>';        
        strRet += '<div class="form-group"><label for="campodia">Campo del dia</label><input type="text" class="form-control" id="campodia" name="campodia" placeholder="dias" required></div>';
        strRet += '<div class="form-group"><label for="camponum">Campo No.Casos</label><input type="text" class="form-control" id="camponum" name="camponum" placeholder="casos" required></div>';
        strRet += '<div class="form-group"><input class="form-control" id="nombreContinente" name="nombreContinente" placeholder="America" type="hidden" value="Continente"></div>';
        strRet += '<div class="form-group"><input class="form-control" id="diasProyeccion" name="diasProyeccion" placeholder="America" type="hidden" value="0"></div>';
        strRet += '<div class="form-group"><input class="form-control" id="camponumIsopado" name="camponumIsopado" placeholder="America" type="hidden" value="camponumIsopado"></div>';
    }else if(valorAnalisis == 3){
        strRet += '<div class="form-group"><label for="campoPaises">Campo de Paises</label><input type="text" class="form-control" id="campoPaises" name="campoPaises" placeholder="Guatemala" required></div>';
        strRet += '<div class="form-group"><label for="nombrePais">Nombre del Pais</label><input type="text" class="form-control" id="nombrePais" name="nombrePais" placeholder="Guatemala" required></div>';        
        strRet += '<div class="form-group"><label for="campodia">Campo del dia</label><input type="text" class="form-control" id="campodia" name="campodia" placeholder="dias" required></div>';
        strRet += '<div class="form-group"><label for="camponum">Campo No.Casos</label><input type="text" class="form-control" id="camponum" name="camponum" placeholder="casos" required></div>';
        strRet += '<div class="form-group"><label for="camponumIsopado">Campo No.Hisopados</label><input type="text" class="form-control" id="camponumIsopado" name="camponumIsopado" placeholder="isopados" required></div>';
        strRet += '<div class="form-group"><label for="diasProyeccion">Dia a obtener el Indice</label><input type="text" class="form-control" id="diasProyeccion" name="diasProyeccion" placeholder="0" required></div>';
        strRet += '<div class="form-group"><input class="form-control" id="nombreContinente" name="nombreContinente" placeholder="America" type="hidden" value="Continente"></div>';        
    }
    strRet += '<br><div class="d-grid gap-2 d-md-flex justify-content-md-end"><button type="submit" class="btn btn-primary">Analizar</button></div>';

    return strRet;
}