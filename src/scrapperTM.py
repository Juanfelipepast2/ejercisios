#TODO ENCONTRAR NACIONALIDAD
import requests
import clases
from bs4 import BeautifulSoup
from PIL import Image
def obtenerJugadorTM(link) -> clases.Jugador:
    try:
        headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

        resultado = requests.get(link, headers=headers)        
        
        
        sopa = BeautifulSoup(resultado.content, "html.parser")

        
                
        nombre = sopa.select_one('h1[class="data-header__headline-wrapper"]').text.split("\n")[-1].strip()
        fechaNacimiento = sopa.select_one('span[itemprop="birthDate"]').text.strip().split(" ")[0]
        estatura = int(float(sopa.select_one('span[itemprop="height"]').text.strip().split(" ")[0].replace(",", ".")) * 100)        
        estado = True if sopa.select_one('span[itemprop="affiliation"]').text.strip() != "Retirado" else False
        #print(nombre)
        #print(fechaNacimiento)
        #print(estatura)        
        #print(estado)
        
        jugador = clases.Jugador(None, 2, nombre, fechaNacimiento, link, estatura, 0 ,None, estado, None)

        arregloPosicionesSoup = sopa.find_all('dd', {"class": "detail-position__position"})

        #TODO OBTENER BINARIOS DE LA FOTO, POR AHORA SERVIRÁ PARA MOSTRARLA ONLINE
        jugador.foto = sopa.select_one('img[class="data-header__profile-image"]').attrs['src']
           
        #iterador                
        i = 0

        #CONTAREMOS LAS VECES QUE UNA POSICION DE BANDA TENGA "IZQUIERDO O DERECHO", ESTO PARA DETERMINAR LA BANDA (SI LOS CONTADORES TERMINAN SIENDO IGUALES, SE PONDRA COMO "AMBAS BANDAS")
        contadorDerechos = 0
        contadorIzquierdos = 0

        #posiciones añadidas
        posicionesAnadidas = []

        for x in arregloPosicionesSoup:          
            if "derecho" in x.string.split():
                contadorDerechos += 1
            elif "izquierdo" in x.string.split():
                contadorIzquierdos += 1

            #AQUI AGREGAMOS LAS POSICIONES AL JUGADOR  
            if  (traducirAbreviatura(x.text.strip()) not in posicionesAnadidas):
                jugador.posiciones.append(clases.Posicion(traducirAbreviatura(x.text.strip()), None, False))
                posicionesAnadidas.append(traducirAbreviatura(x.text.strip()))
            else:
                continue
            #MECANISMO PARA DETERMINAR LA POSICION PRINCIPAL
            if i == 0:
                jugador.posiciones[0].posicionPrincipal = True

            #SI ES LATERAL, TAMBIEN PODRÁ SER CARRILERO
            if jugador.posiciones[i].abreviatura == "CA":   
                jugador.posiciones.append(clases.Posicion("LA", None, False))
                            
            i += 1
        del(i) #BORRAMOS EL i por si lo requierimos despues
        
        if contadorDerechos > contadorIzquierdos:
            jugador.banda = "DER"
        elif contadorDerechos < contadorIzquierdos:
            jugador.banda = "IZQ"
        else:
            jugador.banda = "AMB"
        
        #borramos los contadores
        del(contadorDerechos)   
        del(contadorIzquierdos)
        del(posicionesAnadidas)
        
        
        return jugador

    except (requests.exceptions.RequestException, requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print(e.with_traceback())

def traducirAbreviatura(pos):    
    if pos == "Portero":
        return "PT"
    elif pos == "Defensa central":
        return "CT"
    elif pos == "Lateral izquierdo" or pos == "Lateral derecho":
        return "CA"
    elif pos == "Pivote":
        return "CCD"
    elif pos == "Mediocentro":
        return "CC"
    elif pos == "Interior izquierdo" or pos == "Interior derecho":
        return "VOL"
    elif pos == "Mediocentro ofensivo":
        return "MP"
    elif pos == "Extremo izquierdo" or pos == "Extremo derecho":
        return "EXT"
    elif pos == "Mediapunta":
        return "SD"
    elif pos == "Delantero centro":
        return "DC"                
    else:
        return None
    
obtenerJugadorTM("https://www.transfermarkt.co/konrad-laimer/profil/spieler/223967")
    