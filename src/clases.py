import random
import traceback

import string
import time
import CRUD

class Tecnico:
    def __init__(self, id: int, idPais: int ,nombre: str, apellido: str, contrasena: str, admin, pO):
        self.id = id
        self.idPais = idPais
        self.nombre = nombre
        self.apellido = apellido
        self.contrasena = contrasena
        self.admin = None
        self.pO = None


        self.setAdmin(admin)
        self.setPo(pO)        


    def setAdmin(self, admin):              
        if admin == 'admin':
            self.admin = True
        elif admin == None:
            self.admin = False

    def setPo(self, po):        
        if po == 'owner':
            self.pO = True
        elif po == None:
            self.pO = False

    def __str__(self):
        return f"{self.id} {self.idPais} {self.nombre} {self.apellido} {self.contrasena} {self.admin} {self.pO}"
    
    def iniciarSesion(self, id, contrasena):
        if self.id == id and self.contrasena == contrasena:
            return True
        else:
            return False
    
    def guardarDTecnico(self):
        try:
            con = CRUD.Conexion()
            con.cur.execute("INSERT INTO tecnico (idpais , NOMBRETECNICO, APELLIDOTECNICO, CONTRASENATECNICO, ADMINTECNICO, OWNERTECNICO) VALUES (%s ,%s, %s, %s, %s, %s)", (self.idPais, self.nombre, self.apellido, self.contrasena, self.admin, self.pO))
            con.conexion.commit()
            del con
        except:
            print("Error al guardar el tecnico")


    def obtenerTecnico(id: int):
        tecnicoTemp = None
        try:
            con = CRUD.Conexion()
            con.cur.execute(f"SELECT * FROM tecnico where IDTECNICO = {id}")
            tuplaTecnico = con.cur.fetchone()
            
            if(tuplaTecnico != None):
                tecnicoTemp = Tecnico(int(tuplaTecnico[0]), int(tuplaTecnico[1]), tuplaTecnico[2], tuplaTecnico[3], tuplaTecnico[4], bool(tuplaTecnico[5]), bool(tuplaTecnico[6]))
                            
            
        except:
            print("Error al obtener el tecnico", traceback.print_exc())            
        finally:
            del con
        return tecnicoTemp

    def obtenerContrasena(id: int):
        contraDt = None
        try:
            con = CRUD.Conexion()
            con.cur.execute(f"SELECT CONTRASENATECNICO FROM tecnico where IDTECNICO = {id}")
            contraDt = con.cur.fetchone()[0]                                                                                
        except:
            print("Error al verificar contrasena", traceback.print_exc())            
        finally:
            del con
        return contraDt

    def cantidadTecnicos():
        con = CRUD.Conexion()
        con.cur.execute("SELECT COUNT(*) FROM tecnico")
        cantidad = con.cur.fetchone()[0]
        del con
        return cantidad

class Equipo:
    def __init__(self, id: int, nombre: str, escudo):
        self.id = id
        self.nombre = nombre
        self.escudo = escudo        
        
        ##ATRIBUTOS SIN USAR
        self.presupuesto = None
        self.idTemporada = None
        self.Tecnico: Tecnico = None 

    def setIdTemporada(self, idTemporada: int):
        self.idTemporada = idTemporada
    
    def setPresupuesto(self, presupuesto: int):
        self.presupuesto = presupuesto

    def setTecnico(self, tecnico: Tecnico):
        self.Tecnico = tecnico

    def añadirTecnico(self):
        con = CRUD.Conexion()
        con.cur.execute("insert into tecnicotemporada (IDTECNICO, IDEQUIPO, IDTEMPORADA) values (%s, %s, %s)", (self.Tecnico.id, self.id, self.idTemporada))
        con.conexion.commit()
        del con

class Temporada:
    def __init__(self, id: int, fechaInicio, fechaFin, idPais):
        self.id = id
        self.nombreTemporada = None
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin      


        ###ATRIBUTOS SIN USAR
        self.listaEquipos = []  

    def __str__(self):
        return f"{self.id} {self.fechaInicio} {self.fechaFin} "

    def guardarTemporada(self, idReset):
        con = CRUD.Conexion()
        con.cur.execute("INSERT INTO temporada (IDRESET, NOMBRETEMPORADA, FECHAINICIOTEMPORADA, FECHAFINTEMPORADA) VALUES (%s, %s, %s, %s)", (idReset, self.nombreTemporada ,self.fechaInicio, self.fechaFin))
        con.conexion.commit()
        del con

    def cantidadTemporadas():
        con = CRUD.Conexion()
        con.cur.execute("SELECT COUNT(*) FROM temporada")
        cantidad = con.cur.fetchall()
        del con
        return cantidad[0][0]

    def anadirEquipos(equipo: Equipo):        
        equipo.guardarEquipo()




class Reset:
    def __init__(self, id: int, fechaInicio, fechaFin):
        self.id = id
        self.nombreReset = None
        self.fecha = fechaInicio
        self.fechaFin = fechaFin

    def __str__(self):
        return f"{self.id} {self.nombreReset} {self.fecha} {self.fechaFin}"

    def guardarReset(self):
        con = CRUD.Conexion()
        con.cur.execute("INSERT INTO rreset (NOMBRERESET, FECHAINICIORESET, FECHAFINRESET) VALUES (%s, %s, %s)", (self.nombreReset, self.fechaFin, self.fechaFin))
        con.conexion.commit()
        del con

    def cantidadResets():
        con = CRUD.Conexion()
        con.cur.execute("SELECT COUNT(*) FROM rreset")
        cantidad = con.cur.fetchall()
        del con
        return cantidad[0][0]

    def anadirTemporadas(temporada: Temporada):
        temporada.guardarTemporada(self.id)

