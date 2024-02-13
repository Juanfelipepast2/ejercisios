from flask import Flask, flash, json, jsonify, redirect, request, render_template, url_for, request, session
from functools import wraps
import random, string, clases, traceback



app = Flask(__name__)
app.secret_key = 'Wo7X$Gj79%BBTz'


def sesionRequerida(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if 'codigoDt' in session:
            print("Sesion iniciada")
            return f(*args, **kwargs)
        else:
            print("Sesion no iniciada")
            return redirect(url_for("iniciarSesion"))
    return decorador




@app.route("/")
@sesionRequerida
def inicio():
    
    app.logger.info(f"Se ha cargado la página de inicio {request.path}")
    return render_template("index.html")    



@app.context_processor
def variablesGlobales():
    if 'codigoDt' in session:        
        return {'datosDt': clases.Tecnico.obtenerTecnico(int(session['codigoDt']))}
    else:
        return {'datosDt': None}
    

@app.route("/iniciarSesion", methods=["GET", "POST"])
def iniciarSesion():
    if 'codigoDt' in session:
        return redirect(url_for("inicio"))
    else:
        if request.method == "POST":        
            ##agregamos el usuario
            password = clases.Tecnico.obtenerContrasena(int(request.form.get("codigoDt")))            
            if password != None:
                if password == request.form.get("contrasenaDt"):                    
                    session['codigoDt'] = request.form.get("codigoDt")                
                    return redirect(url_for("inicio"))
                else:
                    flash("Contraseña incorrecta")
                    return render_template("inicioSesion.html")
            else:
                flash("Usuario no encontrado")
                return render_template("inicioSesion.html")
        app.logger.info(f"Se ha cargado la página de inicio de sesi?n {request.path}")
        return render_template("inicioSesion.html")


@app.route("/salir")
@sesionRequerida
def salir():
    session.pop('codigoDt')
    return redirect(url_for("inicio"))

@app.route("/registro")
@sesionRequerida
def registro():    
    
    app.logger.info(f"Se ha cargado la página de registro {request.path}")             
    return render_template("registro.html", cantidadTecnicos=clases.Tecnico.cantidadTecnicos())        

@app.route("/registrandoDt", methods=["POST"])
@sesionRequerida
def registrandoDt():
    if request.method == "POST":
        dtTemp = clases.Tecnico(0, request.form.get('paisNacimiento') ,request.form["nombreDt"], request.form["apellidoDt"], request.form["contrasenaDt"], None, None)
        dtTemp.setAdmin(request.form.get("esAdmin"))
        dtTemp.setPo(request.form.get("esPropietario"))

        print(dtTemp)
        dtTemp.guardarDTecnico()      
        return redirect(url_for("inicio"))


@app.route("/reset/<int:idReset>/temporada/crear")
@sesionRequerida
def crearTemporada(idReset):    
    app.logger.info(f"Se ha cargado la página de creación de temporada {request.path}")
    return render_template("crearTemporada.html", idReset=idReset)

@app.route("/<idReset>/temporada/creandoTemporada", methods=["POST"])
@sesionRequerida
def creandoTemporada(idReset):
    try:
        if request.method == "POST":
            if clases.Reset.obtenerCantidadTemporadas(idReset) == 0:
                #obtenemos los equipos
                equipos = clases.Reset.obtenerEquipos(idReset)            

                #creamos temporada
                temporadaTemp = clases.Temporada(int(request.form['idTemporada']), request.form.get("fechaInicio"), request.form.get("fechaFin"))

                
                for equipo in equipos:
                    #añadimos equipos a la temporada            
                    temporadaTemp.anadirEquipoTemporada(equipo)

                    #añadimos tecnicos a la temporada
                    temporadaTemp.anadirTecnicoTemporada(clases.Tecnico.obtenerTecnico(equipo.tecnico.id))

                temporadaTemp.guardarTemporada(idReset)
            return redirect(url_for("reset", idReset=idReset))
    except:
        return f"ERROR CREANDO TEMPORADA {traceback.print_exc()}"
    return redirect(url_for("temporada"))


@app.route("/temporada/<codigo>")
@sesionRequerida
def partidosTemporada(idTemporada):
    app.logger.info(f"Se ha cargado la página de partidos de la temporada {request.path}")
    return render_template("temporada.html", idTemporada=idTemporada)


@app.route("/temporada")
@app.route("/temporada/<codigo>/<codigoPartido>")
@sesionRequerida
def partido(codigo, codigoPartido):
    app.logger.info(f"Se ha cargado la página de partidos de la temporada {request.path}")
    return render_template("partido.html", codigo=codigo, codigoPartido=codigoPartido)


@app.route("/temporada")
@app.route("/temporada/<codigo>/playoffs")
@sesionRequerida
def playoffs(codigo):
    app.logger.info(f"Se ha cargado la página de playoffs {request.path}")
    return render_template("copas.html", codigo=codigo, title="Playoffs")


@app.route("/temporada")
@app.route("/temporada/<codigo>/progress")
@sesionRequerida
def progress(codigo):
    app.logger.info(f"Se ha cargado la página de playoffs {request.path}")
    return render_template("copas.html", codigo=codigo, title="Progress cup")



@app.route("/reset")
@sesionRequerida
def paginaResets():
    
    resets = clases.Reset.obtenerResets()
    if(resets != None and len(resets) != 0):                
        print(resets)
        print(resets[0].id)
    
    app.logger.info(f"Se ha cargado la página de resets {request.path}")
    return render_template("paginaResets.html", resets=resets)            

@app.route("/reset")
@app.route("/reset/<idReset>")
@sesionRequerida
def reset(idReset):
    app.logger.info(f"Se ha cargado la página de reset {request.path}")
    temporadas = clases.Temporada.obtenerTemporadas(idReset)
    return render_template("temporadasReset.html", idReset=idReset, temporadas=temporadas)

@app.route("/reset/crear")
@sesionRequerida
def crearReset():
    app.logger.info(f"Se ha cargado la página de reset {request.path}")
    codigo = clases.Reset.cantidadResets() + 1
    return render_template("crearReset.html", idReset=codigo, listaTecnicos=(clases.Tecnico.obtenerNombresTecnico()))

@app.route("/reset/<idReset>/creandoReset", methods=["POST"])
@sesionRequerida
def creandoReset(idReset):
    try:        
        if request.method == "POST":
            resetTemp = clases.Reset(idReset, request.form.get("fechaInicio"), request.form.get("fechaFin"))
            
            resetTemp.guardarReset() #guardamos el reset
            cantEquipos = int(request.form.get("cantidadEquipos"))
            for i in range(1, cantEquipos+1):                            
                equipoTemp = clases.Equipo(request.form[f'nombreEquipo{i}'], None, int(idReset), request.form[f'presupuestoEquipo{i}'], int(request.form.get(f'selectorDT{i}')))
                print(equipoTemp)
                resetTemp.anadirEquipo(equipoTemp)
                
            
            return redirect(url_for("crearTemporada", idReset=idReset))
    except Exception as e:
        print(e.with_traceback())
        return redirect(url_for("crearReset"))
    return redirect(url_for("reset", codigo=idReset))






if __name__ == "__main__":
    app.run(debug=True)