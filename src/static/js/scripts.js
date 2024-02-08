



function agregarEquipos(listaTecnicos){    
    console.log(listaTecnicos);
    let cantidadEquipos = document.getElementById('cantidadEquipos');
    const cuerpoTabla = document.getElementById('cuerpoTablaCreacionEquipos');
    const filas = cuerpoTabla.rows;

    cantidadEquipos.value++;
    let tr = document.createElement('tr');


    //SELECTOR DE TECNICOS
    let selectDt = document.createElement('select');
    selectDt.name = 'selectorDT';
    selectDt.id = 'selectorDT';
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
    let cel6 = document.createElement('td');
    let cel7 = document.createElement('td');
    let cel8 = document.createElement('td');
    let cel9 = document.createElement('td');
    
    cel1.innerHTML = `<h4>` + cantidadEquipos.value + `</h4>`;
    cel2.innerHTML = `<input type="text" name="nombreEquipo" id="nombreEquipo" placeholder="Nombre Equipo" required></input>`;
    cel3.innerHTML = `<input type="file" name="botonSelEscudo" id="botonSelEscudo" value="Subir escudo" accept="image/*"></input>`;

    //td del selector
    cel4.innerHTML = `<label for="selectorDT">DT:</label>\n`;
    cel4.appendChild(selectDt);
    //\\\\\\\\\\\\\\\\

    cel5.innerHTML = `<label for="presupuestoEquipo" >Presupuesto Equipo:</label>\n<input type="number" name="presupuestoEquipo" id="presupuestoEquipo" placeholder="Presupuesto" required>`;
    tr.appendChild(cel1);    
    tr.appendChild(cel2);
    tr.appendChild(cel3);
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