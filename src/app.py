from flask import Flask, redirect, request, render_template, url_for, request, session
import random, string, clases

app = Flask(__name__)

app.secret_key = 'Wo7X$Gj79%BBTz'

@app.route("/")
def inicio():
    if 'codigoDt' in session:

        return render_template("index.html")
    return redirect(url_for("iniciarSesion"))

    #app.logger.info(f"Se ha cargado la página de inicio {request.path}")
    #return render_template("index.html")

@app.route("/iniciarSesion", methods=["GET", "POST"])
def iniciarSesion():
    if 'codigoDt' in session:
        return redirect(url_for("inicio"))
    else:
        if request.method == "POST":        
            ##agregamos el usuario
            password = clases.Tecnico.obtenerContrasena(int(request.form.get("codigoDt")))
            if password != None and password == request.form.get("contrasenaDt"):
                session['codigoDt'] = request.form.get("codigoDt")

            return redirect(url_for("inicio"))

        app.logger.info(f"Se ha cargado la página de inicio de sesi?n {request.path}")
        return render_template("inicioSesion.html")


@app.route("/salir")
def salir():
    session.pop('codigoDt')
    return redirect(url_for("inicio"))

@app.route("/registro")
def registro():

    app.logger.info(f"Se ha cargado la p?gina de registro {request.path}")
    contrasena = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))           
    app.logger.info(f"{contrasena} es la contrase?a generada {request.path}")
    return render_template("registro.html", contrasena=contrasena, cantidadTecnicos=clases.Tecnico.cantidadTecnicos())        

@app.route("/registrando_dt", methods=["POST"])
def registrando_dt():
    if request.method == "POST":
        dtTemp = clases.Tecnico(0, request.form.get('paisNacimiento') ,request.form["nombreDt"], request.form["apellidoDt"], request.form["contrasenaDt"], request.form.get("esAdmin"), request.form.get("esPropietario"))
        print(dtTemp)
        dtTemp.guardarDTecnico()
        return redirect(url_for("iniciarSesion"))


@app.route("/temporada/<codigo>")
def partidosTemporada(codigo):
    app.logger.info(f"Se ha cargado la página de partidos de la temporada {request.path}")
    return render_template("temporada.html", codigo=codigo)

@app.route("/crearReset")
def crearReset():
    app.logger.info(f"Se ha cargado la página de reset {request.path}")

    return render_template("crearReset.html")

@app.route("/reset")
@app.route("/reset/<codigo>")
def reset(codigo):
    app.logger.info(f"Se ha cargado la página de reset {request.path}")
    return render_template("temporadasReset.html", codigo=codigo)

@app.route("/temporada")
@app.route("/temporada/<codigo>")
@app.route("/temporada/<codigo>/<codigoPartido>")
def partido(codigo, codigoPartido):
    app.logger.info(f"Se ha cargado la página de partidos de la temporada {request.path}")
    return render_template("partido.html", codigo=codigo, codigoPartido=codigoPartido)



@app.route("/resets")
def paginaResets():
    app.logger.info(f"Se ha cargado la página de resets {request.path}")
    return render_template("paginaResets.html")

@app.route("/temporada")
@app.route("/temporada/<codigo>/playoffs")
def playoffs(codigo):
    app.logger.info(f"Se ha cargado la página de playoffs {request.path}")
    return render_template("copas.html", codigo=codigo, title="Playoffs")


@app.route("/temporada")
@app.route("/temporada/<codigo>/progress")
def progress(codigo):
    app.logger.info(f"Se ha cargado la página de playoffs {request.path}")
    return render_template("copas.html", codigo=codigo, title="Progress cup")

if __name__ == "__main__":
    app.run(debug=True)