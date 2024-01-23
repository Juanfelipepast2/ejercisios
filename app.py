from flask import Flask, redirect, request, render_template, url_for, request
import random, string

app = Flask(__name__)

@app.route("/")
def inicio():
  
    app.logger.info(f"Se ha cargado la página de inicio {request.path}")
    return render_template("index.html")

@app.route("/iniciarSesion")
def iniciarSesion():
    app.logger.info(f"Se ha cargado la página de inicio de sesión {request.path}")
    return render_template("inicioSesion.html")

@app.route("/registro")
def registro():

    app.logger.info(f"Se ha cargado la página de registro {request.path}")
    contrasena = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))           
    app.logger.info(f"{contrasena} es la contraseña generada {request.path}")
    return render_template("registro.html", contrasena=contrasena)        


@app.route("/salir")
def salir():
    app.logger.info(f"Se ha cargado la página de salir {request.path}")
    return redirect(url_for("iniciarSesion"))

@app.route("/temporada")
def partidosTemporada():
    app.logger.info(f"Se ha cargado la página de partidos de la temporada {request.path}")
    return render_template("temporada.html")

@app.route("/reset")
def crearReset():
    app.logger.info(f"Se ha cargado la página de reset {request.path}")

    return render_template("crearReset.html")

@app.route("/reset/<codigo>")
def reset(codigo):
    app.logger.info(f"Se ha cargado la página de reset {request.path}")
    return render_template("temporadasReset.html", codigo=codigo)


if __name__ == "__main__":
    app.run(debug=True)