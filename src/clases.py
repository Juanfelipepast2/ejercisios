import traceback
import datetime

from . import CRUD

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

    def getNombreCompleto(self):    
        return f"{self.nombre} {self.apellido}"

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
    def __init__(self, id: int, idReset: int, nombre: str, escudo, presupuesto: int, idTecnico: int):
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
        equipoTemp = None
        try:
            con = CRUD.Conexion()
            con.cur.execute(f"SELECT * FROM EQUIPOTEMPORADACOMPLETO WHERE IDEQUIPO = {id}")
            equipo = con.cur.fetchone()
            equipoTemp = Equipo(equipo[0], equipo[1], equipo[2], equipo[3], equipo[4], equipo[5])
        except Exception as e:
            print(e)
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
            con.cur.execute(f"SELECT * FROM EQUIPOTEMPORADACOMPLETO WHERE IDTEMPORADA = {idTemporada}")
            equipos = con.cur.fetchall()
            listaEquipos = []
            for(equipo) in equipos:
                equipoTemp = Equipo(equipo[0], equipo[1], equipo[2], equipo[3], equipo[4], equipo[5])                
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
    def __init__(self, id: int, equipoLocal: Equipo, equipoVisitante: Equipo, idTemporada: int, fecha: int, amarillasLocal: int, rojasLocal: int, amarillasVisitante: int, rojasVisitante: int, fase: str, resultado: str):
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
        self.resultado = resultado

        self.golesLocal = []
        self.golesVisitante = []

    


    def serializar(self):
        return {
            "id": self.id,
            "equipoLocal": self.equipoLocal.nombre,
            "equipoVisitante": self.equipoVisitante.nombre,
            "idTemporada": self.idTemporada,
            "fecha": self.fecha,
            "resultado": self.resultado,
            "amarillasLocal": self.amarillasLocal,
            "rojasLocal": self.rojasLocal,
            "amarillasVisitante": self.amarillasVisitante,
            "rojasVisitante": self.rojasVisitante,
            "fase": self.fase
            }                            


    def __str__(self):
        return f"-------------{self.id} {self.equipoLocal} {self.equipoVisitante} {self.idTemporada} {self.fecha} {self.amarillasLocal} {self.rojasLocal} {self.amarillasVisitante} {self.rojasVisitante} {self.fase}"    

    
    def guardarPartido(self):
        try:
            con = CRUD.Conexion()
            con.cur.execute("INSERT INTO PARTIDO (IDTECNICOLOCAL, IDEQUIPOLOCAL, IDTECNICOVISITANTE, IDEQUIPOVISITANTE, IDTEMPORADA, FECHAPARTIDO, AMARILLASLOCALPARTIDO, ROJASLOCALPARTIDO, AMARILLASVISITANTEPARTIDO, ROJASVISITANTEPARTIDO, FASEPARTIDO) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (self.equipoLocal.tecnico.id, self.equipoLocal.id, self.equipoVisitante.tecnico.id, self.equipoVisitante.id, self.idTemporada, self.fecha, self.amarillasLocal, self.rojasLocal, self.amarillasVisitante, self.rojasVisitante, self.fase))
            con.conexion.commit()
        except:
            print(traceback.print_exc())
        finally:
            del con

    def actualizarPartido(self):
        try:
            con = CRUD.Conexion()
            query = f"UPDATE PARTIDO SET AMARILLASLOCALPARTIDO = {self.amarillasLocal}, ROJASLOCALPARTIDO = {self.rojasLocal}, AMARILLASVISITANTEPARTIDO = {self.amarillasVisitante}, ROJASVISITANTEPARTIDO = {self.rojasVisitante}, FASEPARTIDO = '{self.fase}', IDEQUIPOLOCAL = {self.equipoLocal.id}, IDTECNICOLOCAL = {self.equipoLocal.tecnico.id}, IDEQUIPOVISITANTE = {self.equipoVisitante.id} ,IDTECNICOVISITANTE = {self.equipoVisitante.tecnico.id} WHERE IDPARTIDO = {self.id}"
            print(query)
            con.cur.execute(query)
            con.conexion.commit()
            
        except:
            print(traceback.print_exc())
        finally:
            del con

    
    def obtenerPartidosVista(idTemporada: int) -> list:
        try:
            con = CRUD.Conexion()
            con.cur.execute(f"SELECT * FROM PARTIDOCOMPLETO WHERE IDTEMPORADA = {idTemporada}")
            partidos = con.cur.fetchall()
            listaPartidos = []
            for(partido) in partidos:
                equipoTempLocal = Equipo(partido[5], None, partido[4], None, None, partido[5])
                equpoTempVisitante = Equipo(partido[11], None, partido[10], None, None, partido[6])
                listaPartidos.append(Partido(partido[0], equipoTempLocal, equpoTempVisitante, partido[1], partido[2], partido[14], partido[16], partido[15], partido[17], partido[3], resultado = f"{partido[8]} - {partido[9]}")) 
        except:
            print(traceback.print_exc())
        finally:
            del con
        return listaPartidos
    
    def separarResultado(resultado: str) -> list:
        listaResultados = []
        resultados = resultado.split("-")
        for res in resultados:
            res = res.strip()
            listaResultados.append(int(res))

        return listaResultados
    
    def guardarGoles(self):
        for gol in self.golesLocal:
            gol.guardarGol()
        for gol in self.golesVisitante:
            gol.guardarGol()

    @classmethod
    def obtenerPartido(cls, idPartido: int) -> "Partido":	
        partidoTemp = None
        try:
            con = CRUD.Conexion()
            con.cur.execute(f"SELECT * FROM PARTIDOCOMPLETO WHERE IDPARTIDO = {idPartido}")
            partido = con.cur.fetchone()
            equipoTempLocal = Equipo(partido[5], None, partido[4], None, None, partido[6])
            equpoTempVisitante = Equipo(partido[11], None, partido[10], None, None, partido[12])
            partidoTemp = Partido(partido[0], equipoTempLocal, equpoTempVisitante, partido[1], partido[2], partido[14], partido[16], partido[15], partido[17], partido[3], resultado = f"{partido[8]} - {partido[9]}") 
            partidoTemp.golesLocal = Gol.obtenerGolesPartido(idPartido, partidoTemp.equipoLocal.id)
            
            partidoTemp.golesVisitante = Gol.obtenerGolesPartido(idPartido, partidoTemp.equipoVisitante.id)
            print("fase:" + partidoTemp.fase)
            Gol.mostrarGoles(partidoTemp.golesLocal)
            Gol.mostrarGoles(partidoTemp.golesVisitante)

        except:
            print(traceback.print_exc())
        finally:
            del con
        return partidoTemp

    @classmethod
    def obtenerUiltimoIdPartido(cls) -> int:
        id = None
        try:
            con = CRUD.Conexion()
            con.cur.execute("SELECT MAX(IDPARTIDO) FROM PARTIDO")
            id = con.cur.fetchone()[0]
        except:
            print(traceback.print_exc())
        finally:
            del con
        return int(id)

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

class Gol:
    def __init__(self, id: int, idPartido: int, idJugador: int, idTemporada: int, idEquipo: int):
        #TODO GESTIONAR EL NOMBRE DEL JUGADOR QUE ANOTA
        self.id = id
        self.idPartido = idPartido
        self.idJugador = idJugador        
        self.idTemporada = idTemporada
        self.idEquipo = idEquipo

    def __str__(self):
        return f"{self.id} {self.idPartido} {self.idJugador} {self.idTemporada} {self.idEquipo}"

    @classmethod
    def eliminarGolesPartido(cls, idPartido: int):
        try:
            con = CRUD.Conexion()
            con.cur.execute(f"DELETE FROM GOL WHERE IDPARTIDO = {idPartido}")
            con.conexion.commit()
        except:
            print(traceback.print_exc())
        finally:
            del con

    def guardarGol(self):
        try:
            con = CRUD.Conexion()
            con.cur.execute("INSERT INTO GOL (IDPARTIDO, IDJUGADOR, IDTEMPORADA, IDEQUIPO) VALUES (?, ?, ?, ?)", (self.idPartido, self.idJugador, self.idTemporada, self.idEquipo))
            con.conexion.commit()
        except:
            print(traceback.print_exc())
        finally:
            del con


    @classmethod
    def obtenerGolesPartido(cls, idPartido: int, idEquipoAnotador: int): #idEquipoAnotador es el id del equipo que anota
        try:
            con = CRUD.Conexion()
            con.cur.execute(f"SELECT * FROM GOL WHERE IDPARTIDO = {idPartido} AND IDEQUIPO = {idEquipoAnotador}")
            goles = con.cur.fetchall()
            listaGoles = []
            for(gol) in goles:
                listaGoles.append(Gol(gol[0], gol[1], gol[2], gol[3], gol[4]))
        except:
            print(traceback.print_exc())
        finally:
            del con
        return listaGoles
    
    @classmethod
    def mostrarGoles(cls, listaGoles):
        for gol in listaGoles:
            print(gol)

class Stats:
    def __init__(self, idJugador: int):
        self.idJugador = idJugador
        self.ataque: int = 0
        self.defensa: int = 0
        self.estabilidad: int = 0
        self.resistencia: int = 0
        self.velMax: int = 0
        self.aceleracion: int = 0
        self.respuesta: int = 0
        self.agilidad: int = 0
        self.precisionConduccion: int = 0 
        self.velconduccion: int = 0
        self.precPaseCorto: int = 0
        self.velPaseCorto: int = 0
        self.precPaseLargo: int = 0
        self.velPaseLargo: int = 0
        self.precTiro: int = 0        
        self.potTiro: int = 0
        self.tecDisparo: int = 0
        self.precSaqueFalta: int = 0
        self.efecto: int = 0
        self.cabezazo: int = 0
        self.salto: int = 0
        self.tecnica: int = 0
        self.agresividad: int = 0
        self.mentalidad: int = 0
        self.cualidadPortero: int = 0
        self.trabajoEquipo: int = 0
        self.estadoForma: int = 0
        self.precPieMalo: int = 0
        self.frecPieMalo: int = 0
        self.resistenciaLesion: str = "" #o consistencia


        self.habilidades = []
        '''habilidades        
        self.habRegate: bool = False
        self.habRegateHabil: bool = False
        self.habCapPosicion: bool = False
        self.habReaccion: bool = False
        self.habCapMando: bool = False
        self.habPases: bool = False
        self.habGoleadora: bool = False
        self.habGola1: bool = False
        self.habJugadorPoste: bool = False
        self.habLinea: bool = False
        self.habTiroLejano: bool = False
        self.habLado: bool = False
        self.habCentro: bool = False
        self.habLanzaPenales: bool = False
        self.habPase1Toque: bool = False
        self.habExterior: bool = False
        self.habMarcarHombre: bool = False
        self.habBarrida: bool = False
        self.habMarcaje: bool = False
        self.habLineaDefensiva: bool = False
        self.habPorteroPenales: bool = False
        self.habPortero1v1: bool = False
        self.habaSaqueLargo: bool = False
        '''
        
class Posicion:
    def __init__(self, abreviatura: str, idJugador: int, posicionPrincipal:bool) -> None:
        self.abreviatura = abreviatura
        self.idJugador = idJugador
        self.posicionPrincipal = posicionPrincipal

    def __str__(self) -> str:
        return f"{self.abreviatura}" 
        

class Jugador:
    def __init__(self, idJugador: int, idPais: int, nombre: str, fechaNacimiento, linkTransfermarkt: str, estatura: int, peso:int, foto, estadoJugador: bool, banda: str):
        self.idJugador = idJugador
        self.idPais = idPais
        
        self.setNombresYApellidos(nombre)
        self.fechaNacimiento = fechaNacimiento
        self.linkTransfermarkt = linkTransfermarkt
        self.pie = None #DEBEN AGREGARSE DESPUES
        self.estatura = estatura
        self.peso = peso
        self.foto = foto
        self.estadoJugador = estadoJugador        
        self.banda = banda
        self.posiciones: list = []        
        
        self.stats = None #DEBEN AGREGARSE DESPUES                

    def __str__(self):
        return f"{self.idJugador} {self.idPais} {self.nombre} {self.apellido} {self.fechaNacimiento} {self.linkTransfermarkt} {self.pie} {self.estatura} {self.fotoJugador} {self.estadoJugador} {self.banda}"
        
    def obtenerEdad(self):
        diferencia = datetime.datetime.now() - datetime.datetime.strptime(self.fechaNacimiento, "%d/%m/%Y")
        return int(diferencia.days / 365.25)

        
        


    def toJson(self):
        return {
            "idJugador": self.idJugador,
            "idPais": self.idPais,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fechaNacimiento": self.fechaNacimiento,
            "linkTransfermarkt": self.linkTransfermarkt,
            "pie": self.pie,
            "estatura": self.estatura,
            "fotoJugador": self.fotoJugador,
            "estadoJugador": self.estadoJugador,
            "bandaJugador": self.bandaJugador
        }
    
    def setNombresYApellidos(self, texto):
        nombres = texto.split(" ")
        self.nombre = ""
        self.apellido = "" 
        for i in range(len(nombres)):
            if i == 0:
                self.nombre = nombres[i]
            else:
                self.apellido += nombres[i] + " "

    def guardarJugador(self):
        try:
            con = CRUD.Conexion()
            con.cur.execute("INSERT INTO JUGADOR (IDPAIS, NOMBREJUGADOR, APELLIDOJUGADOR, FECHANACIMIENTOJUGADOR, LINKTRANSFERMARKTJUGADOR, PIEJUGADOR, ESTATURAJUGADOR, FOTOJUGADOR, ESTADOJUGADOR, BANDAJUGADOR) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (self.idPais, self.nombre, self.apellido, self.fechaNacimiento, self.linkTransfermarkt, self.pie, self.estatura, self.fotoJugador, self.estadoJugador, self.bandaJugador))
            con.conexion.commit()
        except:
            print(traceback.print_exc())
        finally:
            del con

    def guardarStats(self):
        #TODO guardar stats
        pass
            
class Equipoposiciones:
    def __init__(self):
        self.equipo = None
        self.idTemporada = None
        self.partidosJugados = 0
        self.partidosGanados = 0
        self.partidosEmpatados = 0
        self.partidosPerdidos = 0
        self.golesFavor = 0
        self.golesContra = 0
        self.diffGoles = 0
        self.rendimiento = 0
        self.puntos = 0

    def __str__(self):
        return f"{self.equipo} {self.idTemporada} {self.partidosJugados} {self.partidosGanados} {self.partidosEmpatados} {self.partidosPerdidos} {self.golesFavor} {self.golesContra} {self.diffGoles} {self.rendimiento} {self.puntos}"

    def setEquipo(self, equipo):
        self.equipo = equipo

    @classmethod
    def obtenerListaPosiciones(cls, idTemporada):
        try:
            con = CRUD.Conexion()
            con.cur.execute(f"SELECT * FROM TABLAPOSICIONES WHERE IDTEMPORADA = {idTemporada}")
            posiciones = con.cur.fetchall()
            listaPosiciones = []
            for(posicion) in posiciones:
                posTemp = Equipoposiciones()
                posTemp.equipo = Equipo.obtenerEquipo(posicion[1])
                posTemp.idTemporada = posicion[0]
                posTemp.partidosJugados = posicion[3]
                posTemp.partidosGanados = posicion[4]
                posTemp.partidosEmpatados = posicion[5]
                posTemp.partidosPerdidos = posicion[6]
                posTemp.golesFavor = posicion[7]
                posTemp.golesContra = posicion[8]
                posTemp.diffGoles = posicion[9]
                posTemp.rendimiento = posicion[10]
                posTemp.puntos = posicion[11]
                listaPosiciones.append(posTemp)
        except:
            print(traceback.print_exc())
        finally:
            del con
        return listaPosiciones
    