//FUNCION PARA CAMBIAR CONTRASEÑAS DE DTS
function contrasenaAleatoria(){
    let contrasena = document.getElementById('contrasenaDt');
    const characters ='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let contrasenaGenerada = '';
    for (let i = 0; i < 16; i++){
        contrasenaGenerada += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    contrasena.value = contrasenaGenerada;
}

//FUNCIONES PARA CREAR RESET

function agregarEquipos(listaTecnicos){        
    let cantidadEquipos = document.getElementById('cantidadEquipos');
    const cuerpoTabla = document.getElementById('cuerpoTablaCreacionEquipos');
    const filas = cuerpoTabla.rows;

    cantidadEquipos.value++;
    let tr = document.createElement('tr');


    //SELECTOR DE TECNICOS
    let selectDt = document.createElement('select');
    selectDt.name = 'selectorDT'+cantidadEquipos.value;
    selectDt.id = 'selectorDT'+cantidadEquipos.value;
    selectDt.required = true;
    for (let i = 0; i < listaTecnicos.length; i++) {
        let option = new Option(listaTecnicos[i][1], listaTecnicos[i][0]);        
        selectDt.add(option, undefined);
    }

    //

    let cel1 = document.createElement('td');
    
    let cel2 = document.createElement('td');
    let cel3 = document.createElement('td');
    let cel4 = document.createElement('td');
    let cel5 = document.createElement('td');
    let img = document.createElement('td');
    
    cel1.innerHTML = `<h4>` + cantidadEquipos.value + `</h4><input type='hidden' name='numeroDeEquipo` + cantidadEquipos.value + `' value='` +cantidadEquipos.value+ `'></input>`;    
    cel2.innerHTML = `<input type="text" name="nombreEquipo`+ cantidadEquipos.value +`" id="nombreEquipo`+ cantidadEquipos.value +`" placeholder="Nombre Equipo" required></input>`;
    cel3.innerHTML = `<input type="file" name="botonSelEscudo`+ cantidadEquipos.value +`" id="botonSelEscudo`+ cantidadEquipos.value +`"  accept="image/*" onchange="subirEscudo(this)"><label id="labelBotonImagen" for="botonSelEscudo`+ cantidadEquipos.value +`" >Escudo</label>`;
    img.innerHTML = `<img id='previewEscudo`+ cantidadEquipos.value +`'/>`;

    //td del selector
    cel4.innerHTML = `<label for="selectorDT`+ cantidadEquipos.value +`">DT:</label>\n`;
    cel4.appendChild(selectDt);
    //\\\\\\\\\\\\\\\\

    cel5.innerHTML = `<label for="presupuestoEquipo`+ cantidadEquipos.value +`" >Presupuesto Equipo:</label>\n<input type="number" name="presupuestoEquipo`+ cantidadEquipos.value +`" id="presupuestoEquipo`+ cantidadEquipos.value +`" placeholder="Presupuesto" required>`;
    tr.appendChild(cel1);        
    tr.appendChild(cel2);
    tr.appendChild(cel3);
    tr.appendChild(img);
    tr.appendChild(cel4);
    tr.appendChild(cel5);
    
    

    //tr.innerHTML = codigo;
    //cuerpoTabla.appendChild(tr);
    if(filas.length > 0){
        filas[filas.length - 1].insertAdjacentHTML('beforebegin', tr.innerHTML);
    } else {
        cuerpoTabla.appendChild(tr);
    }
    
    

}

function eliminarEquipos(){
    let cantidadEquipos = document.getElementById('cantidadEquipos');
    const cuerpoTabla = document.getElementById('cuerpoTablaCreacionEquipos');
    const filas = cuerpoTabla.rows;
    if(cantidadEquipos.value > 1){
        cuerpoTabla.deleteRow(cantidadEquipos.value-1);
        cantidadEquipos.value--;
    }
}

function checkPresupuesto(checkbox){    
    let presupuestoGeneral = document.getElementById('presupuestoGeneral');
    let cantEquipos = document.getElementById('cantidadEquipos').value;
    if(checkbox.checked == true){
        for(let i = 1; i <= cantEquipos; i++){
            let presupuestoEquipo = document.getElementById('presupuestoEquipo'+i);
            presupuestoEquipo.readOnly = true;
            presupuestoEquipo.value = presupuestoGeneral.value;
        }
    } else {
        for(let i = 1; i <= cantEquipos; i++){
            let presupuestoEquipo = document.getElementById('presupuestoEquipo'+i);
            presupuestoEquipo.readOnly = false;
            
        }
    }
}

function subirEscudo(botonSelEscudo){        
    console.log(botonSelEscudo.id.slice(-1));
    let previewEscudo = document.getElementById('previewEscudo' + botonSelEscudo.id.slice(-1));
    const [file] = botonSelEscudo.files;
    if(file){
        previewEscudo.src = URL.createObjectURL(file);
        previewEscudo.style.display = 'flex';
    }
}
