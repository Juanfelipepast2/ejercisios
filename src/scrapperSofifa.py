
from bs4 import BeautifulSoup
import requests
from . import clases
import math
from . import scrapperTM as ScrapperTM

def recibirCodigo(codigo, linkTm):
    try:        
        jugador = ScrapperTM.obtenerJugadorTM(linkTm)
               
        headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

        resultado = requests.get(f"https://sofifa.com/player/{codigo}?attr=fut", headers=headers)        
        stats = clases.Stats(None)
        
        sopa = BeautifulSoup(resultado.content, "html.parser")
        

        
        #cambiando cositas del jugador        
        jugador.peso = int(sopa.find('div', class_='profile clearfix').findChild("p").text.strip().split("y.o.")[-1].strip().split()[6].strip().replace("kg", ""))
        jugador.pie = True if sopa.find('label', string='Preferred foot').find_parent("p").text.split(" ", 2)[-1].strip() == "Right" else False

        stats.ataque = int(sopa.find('span', string='Att. Position').find_previous_sibling('em').text.strip())
        ##SE DECLARA PRIMERO LA POTENCIA DEL TIRO PARA QUE SE PUEDA CALCULAR LA VELOCIDAD DE PASES
        stats.potTiro = int(sopa.find('span', string='Shot power').find_previous_sibling('em').text.strip())
        
        stats.defensa = math.ceil((int(sopa.find('span', string='Interceptions').find_previous_sibling('em').text.strip()) + int(sopa.find('span', string='Heading accuracy').find_previous_sibling('em').text.strip()) + int(sopa.find('span', string='Defensive awareness').find_previous_sibling('em').text.strip()) + int(sopa.find('span', string='Standing tackle').find_previous_sibling('em').text.strip()) + int(sopa.find('span', string='Sliding tackle').find_previous_sibling('em').text.strip()))/5)
        stats.estabilidad = int(sopa.find('span', string='Strength').find_previous_sibling('em').text.strip())
        stats.resistencia = int(sopa.find('span', string='Stamina').find_previous_sibling('em').text.strip())
        stats.velMax = int(sopa.find('span', string='Sprint speed').find_previous_sibling('em').text.strip())
        stats.aceleracion = int(sopa.find('span', string='Acceleration').find_previous_sibling('em').text.strip())

        
        stats.respuesta = __hallarRespuesta(jugador.posiciones[0].abreviatura, sopa)

        stats.agilidad = int(sopa.find('span', string='Agility').find_previous_sibling('em').text.strip())
        stats.precisionConduccion = int(sopa.find('span', string='Dribbling').find_previous_sibling('em').text.strip())
        stats.velconduccion = math.ceil((stats.velMax + stats.precisionConduccion)/2)
        stats.precPaseCorto = int(sopa.find('span', string='Short passing').find_previous_sibling('em').text.strip())
        stats.velPaseCorto = math.ceil((stats.potTiro + stats.precPaseCorto)/2)
        stats.precPaseLargo = int(sopa.find('span', string='Long passing').find_previous_sibling('em').text.strip())
        stats.velPaseLargo = math.ceil((stats.potTiro + stats.precPaseLargo)/2)        
        stats.precTiro = int(sopa.find('span', string='Finishing').find_previous_sibling('em').text.strip())        
        ##pot tiro ya está
        stats.tecDisparo = int(sopa.find('span', string='Volleys').find_previous_sibling('em').text.strip())
        stats.precSaqueFalta = int(sopa.find('span', string='FK Accuracy').find_previous_sibling('em').text.strip())

        stats.efecto = int(sopa.find('span', string='Curve').find_previous_sibling('em').text.strip())
        stats.cabezazo = int(sopa.find('span', string='Heading accuracy').find_previous_sibling('em').text.strip())
        stats.salto = int(sopa.find('span', string='Jumping').find_previous_sibling('em').text.strip())
        stats.tecnica = int(sopa.find('span', string='Ball control').find_previous_sibling('em').text.strip())
        stats.agresividad = int(sopa.find('span', string='Aggression').find_previous_sibling('em').text.strip())
        
        stats.mentalidad = int(sopa.find('span', string='Composure').find_previous_sibling('em').text.strip())

        #SE HARÁ UN PROMEDIO DE LAS STATS DE ARQUEROS
        stats.cualidadPortero = math.ceil((int(sopa.find('span', string='GK Diving').find_previous_sibling('em').text.strip()) + int(sopa.find('span', string='GK Handling').find_previous_sibling('em').text.strip()) + int(sopa.find('span', string='GK Reflexes').find_previous_sibling('em').text.strip()) + int(sopa.find('span', string='GK Kicking').find_previous_sibling('em').text.strip()) + int(sopa.find('span', string='GK Positioning').find_previous_sibling('em').text.strip()))/5)

        stats.trabajoEquipo = math.ceil((int(sopa.find('span', string='Vision').find_previous_sibling('em').text.strip()) + stats.mentalidad)/2)

        #hallando estado de forma
        stats.estadoForma = __hallarEstadoForma(sopa)
                
        stats.frecPieMalo = math.ceil((int(sopa.find('label', string='Weak foot').find_parent("p").text.split(" ")[0].strip()))*(8/5))
        stats.precPieMalo = math.ceil((stats.frecPieMalo+stats.tecnica*(8/100))/2)        
        stats.resistenciaLesion = __hallarResistenciaLesiones(stats)
    
        ###STATS BOOLEANAS
        listaEspeciales = __obtenerListaEspeciales(sopa)
        
        if "#Dribbler" in listaEspeciales: stats.habilidades.append("Dribbling")                    ##HAB REGATE
        if (int(sopa.find('label', string='Skill moves').find_parent("p").text.split(" ")[0].strip())) >= 4 : stats.habilidades.append("Tactical dribble")            ##HAB REGATE HABIL
        if ("#Complete midfielder" in listaEspeciales or "#Complete forward" in listaEspeciales or "#Complete defender" in listaEspeciales or "#Tactician" in listaEspeciales or "#Poacher" in listaEspeciales): stats.habilidades.append("Positioning")            ##HAB cap posicion
        if "#Speedster" in listaEspeciales: stats.habilidades.append("Reaction")                    ##HAB REACCION
        if "#Playmaker" in listaEspeciales: stats.habilidades.append("Playmaking")                    ##HAB CAPITAN MANDO
        if ("#Crosser" in listaEspeciales or "#Playmaker" in listaEspeciales): stats.habilidades.append("Passing")                    ##HAB PASES
        if ("#Aerial threat" in listaEspeciales or "#Poacher" in listaEspeciales or "#Distance shooter" in listaEspeciales or "#FK specialist" in listaEspeciales) and "#Clinical finisher" in listaEspeciales: stats.habilidades.append("Scoring")                ##HAB goleadora
        if "#Clinical finisher" in listaEspeciales : stats.habilidades.append("1-1 scoring")                    ##HAB GOLA 1V1
        if "#Tactician" in listaEspeciales: stats.habilidades.append("Post player")                    ##HAB JUGADOR POSTE
        if ("Post player" in stats.habilidades and ("CT" in jugador.posiciones)): stats.habilidades.append("Df positioning")                    ##HAB LINEA
        if ("#Distance shooter" in listaEspeciales or "#FK specialist" in listaEspeciales): stats.habilidades.append("Middle shooting")                    ##HAB TIRO LEJANO  
        if (("EXT" in jugador.posiciones or "VOL" in jugador.posiciones or "CA" in jugador.posiciones) and stats.velMax >= 80): stats.habilidades.append("Side")                    ##HAB LADO
        if (("CCD" in jugador.posiciones or "CC" in jugador.posiciones or "MP" in jugador.posiciones or "SD" in jugador.posiciones) and stats.respuesta >= 80): stats.habilidades.append("Centre")                    ##HAB CENTRO
        if (("#FK specialist" in listaEspeciales and stats.precSaqueFalta >=85) or ("#Distance shooter" in listaEspeciales or "#FK specialist" in listaEspeciales)): stats.habilidades.append("Penalties")                    ##HAB LANZA PENALES
        if ("#Playmaker" in listaEspeciales and stats.precPaseCorto >= 82): stats.habilidades.append("1-Touch pass")                    ##HAB PASE 1 TOQUE
        if (stats.velMax > 82 and stats.agilidad >=85): stats.habilidades.append("Outside")                    ##HAB EXTERIOR
        if ("#Tackling" in listaEspeciales or stats.defensa >= 87): stats.habilidades.append("Marking")                    ##HAB MARCAR HOMBRE
        if ("#Tackling" in listaEspeciales): stats.habilidades.append("Sliding tackle")                    ##HAB BARRIDA
        if ("Positioning" in stats.habilidades or stats.defensa >= 83): stats.habilidades.append("Covering")                    ##HAB MARCAJE
        if ("Covering" in stats.habilidades and stats.defensa >= 85): stats.habilidades.append("D-line control")                    ##HAB LINEA DEFENSIVA
        if (stats.respuesta >= 85 and stats.cualidadPortero >= 85): stats.habilidades.append("Penalty stopper")                    ##HAB PORTERO PENALES
        if (stats.respuesta >= 83 and stats.cualidadPortero >= 82): stats.habilidades.append("1-1 Stopper")                    ##HAB PORTERO 1V1
        if (stats.velPaseLargo >= 85): stats.habilidades.append("Long throw")                    ##HAB SAQUE LARGO

        #stats.habRegate = True if "#Dribbler" in listaEspeciales else False
        #stats.habRegateHabil = True if (int(sopa.find('label', string='Skill moves').find_parent("p").text.split(" ")[0].strip())) >= 4 else False
        #stats.habCapPosicion = True if ("#Complete midfielder" in listaEspeciales or "#Complete forward" in listaEspeciales or "#Complete defender" in listaEspeciales or stats.habJugadorPoste or "#Poacher" in listaEspeciales)  else False
        #stats.habJugadorPoste = True if "#Tactician" in listaEspeciales else False
        #stats.habReaccion = True if "#Speedster" in listaEspeciales else False
        #stats.habCapMando = True if "#Playmaker" in listaEspeciales else False
        #stats.habPases = True if ("#Crosser" in listaEspeciales or stats.habCapMando) else False
        #stats.habTiroLejano = True if ("#Distance shooter" in listaEspeciales or "#FK specialist" in listaEspeciales) else False
        #stats.habGola1v1 = True if "#Clinical finisher" in listaEspeciales else False
        #stats.habGoleadora = True if ("#Aerial threat" in listaEspeciales or "#Poacher" in listaEspeciales or stats.habTiroLejano or stats.habGola1v1) else False        
        #stats.habLinea = True if (stats.habJugadorPoste and ("CT" in jugador.posiciones) ) else False
        #stats.habLado = True if (("EXT" in jugador.posiciones or "VOL" in jugador.posiciones or "CA" in jugador.posiciones) and stats.velMax >= 80) else False
        #stats.habCentro = True if (("CCD" in jugador.posiciones or "CC" in jugador.posiciones or "MP" in jugador.posiciones or "SD" in jugador.posiciones) and stats.respuesta >= 80) else False
        #stats.habLanzaPenales = True if ("#FK specialist" in listaEspeciales or stats.precSaqueFalta >=85 or stats.habGoleadora) else False
        #stats.habPase1Toque = True if (stats.habCapMando and stats.precPaseCorto >= 84) else False
        #stats.habExterior = True if (stats.precTiro > 85, stats.agilidad >=85) else False
        #stats.habMarcarHombre = True if (stats.habBarrida or stats.defensa >= 87) else False        
        #stats.habBarrida = True if ("#Tackling" in listaEspeciales) else False
        #stats.habMarcaje = True if (stats.habCapPosicion or stats.defensa >= 83) else False
        #stats.habLineaDefensiva = True if (stats.habMarcaje and stats.defensa >= 85) else False
        #stats.habPorteroPenales = True if (stats.respuesta >= 85 and stats.cualidadPortero >= 85) else False
        #stats.habPortero1v1 = True if (stats.respuesta >= 83 and stats.cualidadPortero >= 82) else False
        #stats.habaSaqueLargo = True if (stats.velPaseLargo >= 85) else False
                
        del(listaEspeciales)
        jugador.stats = stats
            
        return jugador
                

        
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print(e.with_traceback())
    


def __hallarEstadoForma(sopa):
    workRateTxt = (sopa.find('label', string='Work rate').find_parent("p").text.split(" ", 2)[-1].strip())
    if workRateTxt == "Low/ Low":
        return 4
    elif workRateTxt == "Medium/ Low":
        return 5
    elif workRateTxt == "Medium/ Medium":
        return 6
    elif workRateTxt == "High/ Medium":
        return 7
    elif workRateTxt == "High/ High":
        return 8
        
def __hallarRespuesta(posicionJugador, sopa):
    return int(sopa.find('span', string='GK Reflexes').find_previous_sibling('em').text.strip()) if posicionJugador == "PT" else int(sopa.find('span', string='Reactions').find_previous_sibling('em').text.strip())
    
def __hallarResistenciaLesiones(stats):
    sumaTemporal =stats.resistencia + stats.estabilidad
    return "A" if sumaTemporal >= 160 else "B" if (sumaTemporal <= 160 and sumaTemporal >=140) else "C" 

def __obtenerListaEspeciales(sopa):
    especiales = sopa.find('h5', string='Player specialities').find_next_siblings("p")
    listaEspeciales = []
    for x in especiales:
        listaEspeciales.append(x.text.strip())
    return listaEspeciales
    
    
    
#recibirCodigo(252371, "https://www.transfermarkt.co/jude-bellingham/profil/spieler/581678")