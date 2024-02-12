import random
import traceback

import string
import time
import CRUD

class Tecnico:
    def __init__(self, id: int, idPais: int ,nombre: str, apellido: str, contrasena: str, admin: bool, pO: bool):
        self.id = id
        self.idPais = idPais
        self.nombre = nombre
        self.apellido = apellido
        self.contrasena = contrasena
        self.admin = admin
        self.pO = pO


     

    def toJson(self):
        return {
            "id": self.id,
            "idPais": self.idPais,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "contrasena": self.contrasena,
            "admin": self.admin,
            "pO": self.pO
        }


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
            con.cur.execute("INSERT INTO TECNICO (IDPAIS , NOMBRETECNICO, APELLIDOTECNICO, CONTRASENATECNICO, ADMINTECNICO, OWNERTECNICO) VALUES (? , ?, ?, ?, ?, ?)", (self.idPais, self.nombre, self.apellido, self.contrasena, self.admin, self.pO))
            con.conexion.commit()
            del con
        except:
            print("Error al guardar el tecnico")
            print(traceback.print_exc())


    def obtenerTecnico(id: int):
        tecnicoTemp = None
        con = None
        try:
            con = CRUD.Conexion()
            con.cur.execute(f"SELECT * FROM TECNICO where IDTECNICO = {id}")
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
            con.cur.execute(f"SELECT CONTRASENATECNICO FROM TECNICO where IDTECNICO = {id}")
            contraDt = con.cur.fetchone()[0]                                                                                
        except:
            print("Error al verificar contrasena", traceback.print_exc())            
        finally:
            del con
        return contraDt

    def cantidadTecnicos():
        con = CRUD.Conexion()
        con.cur.execute("SELECT COUNT(*) FROM TECNICO")
        cantidad = con.cur.fetchone()[0]
        del con
        return cantidad

    def obtenerNombresTecnico():
        con = CRUD.Conexion()
        con.cur.execute("SELECT IDTECNICO , NOMBRETECNICO, APELLIDOTECNICO FROM TECNICO")
        dts = con.cur.fetchall()
        listaNombres = []
        for dt in dts:
            listaNombres.append([ dt[0], f"{dt[1]} {dt[2]}"])
        del con
        return listaNombres

class Equipo:
    def __init__(self, nombre: str, escudo, idReset: int, presupuesto: int, idTecnico: int):
        self.id = None
        self.nombre = nombre
        self.escudo = escudo        
        self.idReset = idReset
        self.presupuesto = presupuesto
        
        #ATRIBUTOS CON METODOS
        self.setTecnico(idTecnico)
        ##ATRIBUTOS SIN USAR
        
        
        
        self.idTemporada = None        

    
    

    def setTecnico(self, idTecnico: int) -> Tecnico:
        self.tecnico = Tecnico.obtenerTecnico(idTecnico)

    def __str__(self) -> str:
        return f'{self.id} {self.nombre} {self.escudo} {self.idReset} {self.presupuesto} {self.tecnico}'
    
    

class Temporada:
    def __init__(self, id: int, fechaInicio, fechaFin):
        self.id = id
        self.nombreTemporada = ''
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin      


        ###ATRIBUTOS SIN USAR
        self.listaEquipos = []  

    def __str__(self):
        return f"{self.id} {self.fechaInicio} {self.fechaFin} "

    def guardarTemporada(self, idReset):
        try:
            con = CRUD.Conexion()
            con.cur.execute("INSERT INTO TEMPORADA (IDTEMPORADA, IDRESET, NOMBRETEMPORADA, FECHAINICIOTEMPORADA, FECHAFINTEMPORADA) VALUES (?, ?, ?, ?, ?)", (self.id ,idReset, self.nombreTemporada ,self.fechaInicio, self.fechaFin))
            con.conexion.commit()
        except:
            print(traceback.print_exc())
        finally:
            del con

    def cantidadTemporadas():
        try:
            con = CRUD.Conexion()
            con.cur.execute("SELECT COUNT(*) FROM TEMPORADA")
            cantidad = con.cur.fetchall()
            
        except:
            print(traceback.print_exc())
        finally:
            del con
        return cantidad[0][0]
    
    def obtenerTemporadas(idReset: int):
        try:
            con = CRUD.Conexion()
            con.cur.execute(f"SELECT * FROM TEMPORADA WHERE IDRESET = {idReset}")
            temporadas = con.cur.fetchall()
            listaTemporadas = []
            for(temporada) in temporadas:
                listaTemporadas.append(Temporada(temporada[0], temporada[3], temporada[4]))
        except:
            print(traceback.print_exc())
        finally:
            del con
        return listaTemporadas

    def anadirTecnicoTemporada(self, tecnico: Tecnico):
        try:
            con = CRUD.Conexion()
            con.cur.execute("INSERT INTO TECNICOTEMPORADA (IDTECNICO, IDEQUIPO, IDTEMPORADA) VALUES (?, ?, ?)", (tecnico.tecnico.id, tecnico.id, self.id))
            con.conexion.commit()
            del con
        except:
            print(traceback.print_exc())
        finally:
            del con

    def anadirEquipoTemporada(self, equipo: Equipo):
        try:
            con = CRUD.Conexion()
            con.cur.execute("INSERT INTO EQUIPOPORTEMPORADA (IDTEMPORADA, IDEQUIPO, PRESUPUESTO) VALUES (?, ?, ?)", (self.id, equipo.id, equipo.presupuesto))
            con.conexion.commit()
            del con
        except:
            print(traceback.print_exc())
        finally:
            del con

    

class Reset:
    def __init__(self, id: int, fechaInicio, fechaFin):
        self.id = id
        self.nombreReset = ''
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin

        if fechaFin == '':
            self.fechaFin = None


    def __str__(self):
        return f"{self.id} {self.nombreReset} {self.fechaInicio} {self.fechaFin}"

    def guardarReset(self):
        try:
            con = CRUD.Conexion()
            con.cur.execute("INSERT INTO RRESET (NOMBRERESET, FECHAINICIORESET, FECHAFINRESET) VALUES (?, ?, ?)", (self.nombreReset, self.fechaInicio, self.fechaFin))
            con.conexion.commit()
        except:
            print(traceback.print_exc())
        finally:
            del con

    def cantidadResets():
        cantidad = None
        try:
            con = CRUD.Conexion()
            con.cur.execute("SELECT COUNT(*) FROM RRESET")
            cantidad = con.cur.fetchall()
        except:
            print(traceback.print_exc())
        finally:
            del con
        return cantidad[0][0]
    
    def obtenerResets():        
        try:
            con = CRUD.Conexion()
            con.cur.execute("SELECT * FROM RRESET")
            resets = con.cur.fetchall()
            listaResets = []
            for(reset) in resets:
                listaResets.append(Reset(reset[0], reset[2], reset[3]))
            print(resets)
        except:
            print(traceback.print_exc())
        finally:
            del con
        return listaResets
    
    def anadirEquipo(self, equipo: Equipo):
        try:
            print(equipo)
            con = CRUD.Conexion()
            con.cur.execute("INSERT INTO EQUIPO (`NOMBREEQUIPO`, `ESCUDOEQUIPO`, `IDRESET`, `PRESUPUESTOINICIAL`, `IDTECNICO`) VALUES (?, ?, ?, ?, ?)", (equipo.nombre, equipo.escudo, equipo.idReset, equipo.presupuesto, equipo.tecnico.id))
            con.conexion.commit()
            
        except:
            print(traceback.print_exc())
        finally:
            del con
    
    def obtenerUltimoIdReset():
        id = None
        try:
            con = CRUD.Conexion()
            con.cur.execute("SELECT MAX(IDRESET) FROM RRESET")
            id = con.cur.fetchone()[0]
        except:
            print(traceback.print_exc())
        finally:
            del con
        return id

    def obtenerEquipos(idReset: int):
        try:
            con = CRUD.Conexion()
            con.cur.execute(f"SELECT * FROM EQUIPO WHERE IDRESET = {idReset}")
            equipos = con.cur.fetchall()
            listaEquipos = []
            for(equipo) in equipos:
                listaEquipos.append(Equipo(equipo[1], equipo[2], equipo[3], equipo[4], equipo[5]))
        except:
            print(traceback.print_exc())
        finally:
            del con
        return listaEquipos
    
    def obtenerCantidadTemporadas(idReset: int):
        try:
            con = CRUD.Conexion()
            con.cur.execute(F"SELECT COUNT(*) FROM TEMPORADA WHERE IDRESET = {idReset}")
            cantidad = con.cur.fetchall()
        except:
            print(traceback.print_exc())
        finally:
            del con
        return cantidad[0][0]
