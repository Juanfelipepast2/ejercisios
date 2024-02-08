from flask import Flask, flash, json, jsonify, redirect, request, render_template, url_for, request, session
from functools import wraps
import random, string, clases



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
    
    app.logger.info(f"Se ha cargado la p?gina de registro {request.path}")
    contrasena = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))           
    app.logger.info(f"{contrasena} es la contrase?a generada {request.path}")
    return render_template("registro.html", contrasena=contrasena, cantidadTecnicos=clases.Tecnico.cantidadTecnicos())        

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


@app.route("/temporada/<codigo>")
@sesionRequerida
def partidosTemporada(codigo):
    app.logger.info(f"Se ha cargado la página de partidos de la temporada {request.path}")
    return render_template("temporada.html", codigo=codigo)


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
    app.logger.info(f"Se ha cargado la página de resets {request.path}")
    return render_template("paginaResets.html")

@app.route("/reset")
@app.route("/reset/<codigo>")
@sesionRequerida
def reset(codigo):
    app.logger.info(f"Se ha cargado la página de reset {request.path}")
    return render_template("temporadasReset.html", codigo=codigo)

@app.route("/reset/<codigo>/crear")
@sesionRequerida
def crearReset(codigo):
    app.logger.info(f"Se ha cargado la página de reset {request.path}")



    return render_template("crearReset.html", codigo=codigo, listaTecnicos=(clases.Tecnico.obtenerNombresTecnico()))






if __name__ == "__main__":
    app.run(debug=True)