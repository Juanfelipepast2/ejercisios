from flask import Flask, redirect, request, render_template, url_for

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
    return render_template("registro.html")

@app.route("/salir")
def salir():
    app.logger.info(f"Se ha cargado la página de salir {request.path}")
    return redirect(url_for("iniciarSesion"))