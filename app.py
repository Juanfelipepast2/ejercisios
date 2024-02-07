from flask import Flask, redirect, request, render_template, url_for, request
import random, string, clases

app = Flask(__name__)

@app.route("/")
def inicio():
  
    app.logger.info(f"Se ha cargado la página de inicio {request.path}")
    return render_template("index.html")

@app.route("/iniciarSesion")
def iniciarSesion():
    app.logger.info(f"Se ha cargado la página de inicio de sesi?n {request.path}")
    return render_template("inicioSesion.html")

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


@app.route("/salir")
def salir():
    app.logger.info(f"Se ha cargado la página de salir {request.path}")
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