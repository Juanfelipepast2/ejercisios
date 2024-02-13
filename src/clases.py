import traceback

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

    def __str__(self):
        return f"{self.id} {self.idPais} {self.nombre} {self.apellido} {self.contrasena} {self.admin} {self.pO}"
     

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
    
    
    
    def guardarTecnico(self):
        try:
            con = CRUD.Conexion()
            con.cur.execute("INSERT INTO TECNICO (IDPAIS , NOMBRETECNICO, APELLIDOTECNICO, CONTRASENATECNICO, ADMINTECNICO, OWNERTECNICO) VALUES (? , ?, ?, ?, ?, ?)", (self.idPais, self.nombre, self.apellido, self.contrasena, self.admin, self.pO))
            con.conexion.commit()
            del con
        except:
            print("Error al guardar el tecnico")
            print(traceback.print_exc())

    def guardarTecnicoTemporada(self, idTemporada: int, idEquipo: int):
        try:
            con = CRUD.Conexion()
            con.cur.execute("INSERT INTO TECNICOTEMPORADA (IDTECNICO, IDEQUIPO, IDTEMPORADA) VALUES (?, ?, ?)", (self.id, idEquipo, idTemporada))
            con.conexion.commit()
            
        except:
            print("Error al guardar el tecnico")
            print(traceback.print_exc())
        finally:
            del con


    @classmethod
    def obtenerTecnico(cls, id: int):
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

    @classmethod
    def __obtenerContrasena(cls, id: int):
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
    
    @classmethod
    def iniciarSesion(cls, id, contrasena):
        if contrasena == None:
            return None
        elif cls.__obtenerContrasena(id) == contrasena:            
            return True        
        return False
        
            

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
    def __init__(self, id: int, idReset: int, idTecnico: int, nombre: str, escudo, presupuesto: int):
        self.id = id
        self.nombre = nombre
        self.escudo = escudo        
        self.idReset = idReset
        self.presupuesto = presupuesto
        
        #ATRIBUTOS CON METODOS
        self.setTecnico(idTecnico)
        ##ATRIBUTOS SIN USAR
                
    def setTecnico(self, idTecnico: int) -> Tecnico:
        self.tecnico: Tecnico = Tecnico.obtenerTecnico(idTecnico)

    def __str__(self) -> str:
        return f'{self.id} {self.nombre} {self.escudo} {self.idReset} {self.presupuesto} {self.tecnico}'
    
    def guardarJugadores():
        pass

    def guardarEquipo(self):
        try:
            con = CRUD.Conexion()
            con.cur.execute("INSERT INTO EQUIPO (IDRESET, IDTECNICO, NOMBREEQUIPO, ESCUDOEQUIPO, PRESUPUESTOINICIAL) VALUES (?, ?, ?, ?, ?)", (self.idReset, self.tecnico.id, self.nombre, self.escudo, self.presupuesto))
            con.conexion.commit()
        except:
            print(traceback.print_exc())
        finally:
            del con


    def guardarEquipoTemporada(self, idTemporada):
        try:
            con = CRUD.Conexion()
            con.cur.execute("INSERT INTO EQUIPOTEMPORADA (IDTEMPORADA, IDEQUIPO, PRESUPUESTO) VALUES (?, ?, ?)", (idTemporada, self.id, self.presupuesto))
            con.conexion.commit()            
        except:
            print(traceback.print_exc())
        finally:
            del con

    @classmethod
    def obtenerEquipos(cls, idReset: int):
        try:
            con = CRUD.Conexion()
            con.cur.execute(f"SELECT * FROM EQUIPO WHERE IDRESET = {idReset}")
            equipos = con.cur.fetchall()
            listaEquipos = []
            for(equipo) in equipos:
                listaEquipos.append(Equipo(equipo[0], equipo[1], equipo[2], equipo[3], equipo[4], equipo[5]))
        except:
            print(traceback.print_exc())
        finally:
            del con
        return listaEquipos

    
    
    

class Temporada:
    def __init__(self, id: int, idResest: int, fechaInicio, fechaFin):
        self.id = id
        self.idReset = idResest
        self.nombreTemporada = ''
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin      



    def __str__(self):
        return f"{self.id} {self.idReset} {self.fechaInicio} {self.fechaFin} "

    def guardarTemporada(self):
        try:
            con = CRUD.Conexion()
            con.cur.execute("INSERT INTO TEMPORADA (IDTEMPORADA, IDRESET, NOMBRETEMPORADA, FECHAINICIOTEMPORADA, FECHAFINTEMPORADA) VALUES (?, ?, ?, ?, ?)", (self.id, self.idReset, self.nombreTemporada ,self.fechaInicio, self.fechaFin))
            con.conexion.commit()
        except:
            print(traceback.print_exc())
        finally:
            del con
    
    def obtenerTemporadas(idReset: int):
        try:
            con = CRUD.Conexion()
            con.cur.execute(f"SELECT * FROM TEMPORADA WHERE IDRESET = {idReset}")
            temporadas = con.cur.fetchall()
            listaTemporadas = []
            for(temporada) in temporadas:
                listaTemporadas.append(Temporada(temporada[0], temporada[1], temporada[3], temporada[4]))
        except:
            print(traceback.print_exc())
        finally:
            del con
        return listaTemporadas
    
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

    
    
    
