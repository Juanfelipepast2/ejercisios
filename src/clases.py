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
        if id != None:
            try:
                con = CRUD.Conexion()
                con.cur.execute(f"SELECT * FROM TECNICO where IDTECNICO = {int(id)}")
                tuplaTecnico = con.cur.fetchone()
                
                if(tuplaTecnico != None):
                    tecnicoTemp = Tecnico(int(tuplaTecnico[0]), int(tuplaTecnico[1]), tuplaTecnico[2], tuplaTecnico[3], tuplaTecnico[4], bool(tuplaTecnico[5]), bool(tuplaTecnico[6]))
                                
                
            except:
                print("Error al obtener el tecnico", traceback.format_exc())            
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

    @classmethod
    def obtenerTecnicosTemporada(cls, idTemporada, idEquipo):
        try:
            con = CRUD.Conexion()
            con.cur.execute(f"SELECT IDTECNICO FROM TECNICOTEMPORADA WHERE IDTEMPORADA = {idTemporada} AND IDEQUIPO = {idEquipo}")
            dt = con.cur.fetchone()
            
            
            dtTemp = (cls.obtenerTecnico(dt[0]))
        except:
            print(traceback.print_exc())
        finally:
            del con
        return dtTemp
    
    @classmethod
    def obtenerTecnicos(cls):
        try:
            con = CRUD.Conexion()
            con.cur.execute("SELECT * FROM TECNICO")
            dts = con.cur.fetchall()
            listaDts = []
            for(dt) in dts:
                listaDts.append(Tecnico(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5], dt[6]))
        except:
            print(traceback.print_exc())
        finally:
            del con
        return listaDts
        

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
        return f'{self.id} {self.nombre} {self.escudo} {self.idReset} {self.presupuesto} {self.tecnico} {self.escudo}'
    
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
    def obtenerEquipo(cls, id):
        try:
            con = CRUD.Conexion()
            con.cur.execute(f"SELECT * FROM EQUIPO WHERE IDEQUIPO = {id}")
            equipo = con.cur.fetchone()
            equipoTemp = Equipo(equipo[0], equipo[1], equipo[2], equipo[3], equipo[4], equipo[5])              
        except:
            print(traceback.print_exc())
        finally:
            del con
        return equipoTemp


    @classmethod
    def obtenerEquiposReset(cls, idReset: int):
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
    
    @classmethod
    def obtenerEquiposTemporada(cls, idTemporada: int):
        try:
            con = CRUD.Conexion()
            con.cur.execute(f"SELECT * FROM EQUIPO WHERE IDEQUIPO IN (SELECT IDEQUIPO FROM EQUIPOTEMPORADA WHERE IDTEMPORADA = {idTemporada})")
            equipos = con.cur.fetchall()
            listaEquipos = []
            for(equipo) in equipos:
                equipoTemp = Equipo(equipo[0], equipo[1], None, equipo[3], equipo[4], equipo[5])                
                equipoTemp.tecnico = Tecnico.obtenerTecnicosTemporada(idTemporada, equipoTemp.id)
                listaEquipos.append(equipoTemp)

                              
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

class Partido:
    def __init__(self, id: int, equipoLocal: Equipo, equipoVisitante: Equipo, idTemporada: int, fecha: int, amarillasLocal: int, rojasLocal: int, amarillasVisitante: int, rojasVisitante: int, fase: str):
        self.id = id
        self.equipoLocal = equipoLocal
        self.equipoVisitante = equipoVisitante
        self.idTemporada = idTemporada
        self.fecha = fecha
        self.amarillasLocal = amarillasLocal
        self.rojasLocal = rojasLocal
        self.amarillasVisitante = amarillasVisitante
        self.rojasVisitante = rojasVisitante
        self.fase = fase

    def __str__(self):
        return f"{self.id} {self.equipoLocal} {self.equipoVisitante} {self.idTemporada} {self.fecha} {self.amarillasLocal} {self.rojasLocal} {self.amarillasVisitante} {self.rojasVisitante} {self.fase}"
    
    def guardarPartido(self):
        try:
            con = CRUD.Conexion()
            con.cur.execute("INSERT INTO PARTIDO (IDTECNICOLOCAL, IDEQUIPOLOCAL, IDTECNICOVISITANTE, IDEQUIPOVISITANTE, IDTEMPORADA, FECHAPARTIDO, AMARILLASLOCALPARTIDO, ROJASLOCALPARTIDO, AMARILLASVISITANTEPARTIDO, ROJASVISITANTEPARTIDO, FASEPARTIDO) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (self.equipoLocal.tecnico.id, self.equipoLocal.id, self.equipoVisitante.tecnico.id, self.equipoVisitante.id, self.idTemporada, self.fecha, self.amarillasLocal, self.rojasLocal, self.amarillasVisitante, self.rojasVisitante, self.fase))
            con.conexion.commit()
        except:
            print(traceback.print_exc())
        finally:
            del con

    def obtenerPartidosTemporada(idTemporada: int):
        try:
            con = CRUD.Conexion()
            con.cur.execute(f"SELECT * FROM PARTIDO WHERE IDTEMPORADA = {idTemporada}")
            partidos = con.cur.fetchall()
            listaPartidos = []
            for(partido) in partidos:
                listaPartidos.append(Partido(partido[0], Equipo.obtenerEquipo(partido[2]), Equipo.obtenerEquipo(partido[4]), partido[5], partido[6], partido[7], partido[8], partido[9], partido[10], partido[11]))
        except:
            print(traceback.print_exc())
        finally:
            del con
        return listaPartidos
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

class gol:
    def __init__(self, id: int, idPartido: int, idJugador: int, idTemporada: int, idEquipo: int):
        self.id = id
        self.idPartido = idPartido
        self.idJugador = idJugador        
        self.idTemporada = idTemporada
        self.idEquipo = idEquipo

    def __str__(self):
        return f"{self.id} {self.idPartido} {self.idJugador} {self.idTemporada} {self.idEquipo}"

    def guardarGol(self):
        try:
            con = CRUD.Conexion()
            con.cur.execute("INSERT INTO GOL (IDPARTIDO, IDJUGADOR, IDTEMPORADA, IDEQUIPO) VALUES (?, ?, ?, ?)", (self.idPartido, self.idJugador, self.idTemporada, self.idEquipo))
            con.conexion.commit()
        except:
            print(traceback.print_exc())
        finally:
            del con

    def obtenerGolesPartido(idPartido: int):
        try:
            con = CRUD.Conexion()
            con.cur.execute(f"SELECT * FROM GOL WHERE IDPARTIDO = {idPartido}")
            goles = con.cur.fetchall()
            listaGoles = []
            for(gol) in goles:
                listaGoles.append(gol(gol[0], gol[1], gol[2], gol[3], gol[4]))
        except:
            print(traceback.print_exc())
        finally:
            del con
        return listaGoles
    
    
