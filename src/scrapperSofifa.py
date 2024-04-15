#TODO terminar stats booleanas
#TODO FALTA RESPUESTA DEPENDIENDO DE POSICIÓN (SI ES ARQUERO O NO Y SI ES DEFENSA) (ATTACKING POSSITION, GK Reflexes)
#TODO encontrar posiciones principales y secundarias

from bs4 import BeautifulSoup
import requests
import clases
import math

def recibirCodigo(codigo, jugador: clases.Jugador):
    try:

        headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

        resultado = requests.get(f"https://sofifa.com/player/{codigo}?attr=fut", headers=headers)        
        stats = clases.Stats(None)
        
        sopa = BeautifulSoup(resultado.content, "html.parser")
        
        #cambiando cositas del jugador
        jugador.pie = True if sopa.find('label', string='Preferred foot').find_parent("p").text.split(" ", 2)[-1].strip() == "Right" else False


        ##SE DECLARA PRIMERO LA POTENCIA DEL TIRO PARA QUE SE PUEDA CALCULAR LA VELOCIDAD DE PASES
        stats.potTiro = int(sopa.find('span', string='Shot power').find_previous_sibling('em').text.strip())
        #stats.ataque = int(sopa.select_one('span[class="bp3-tag p p-80"]').text.strip())
        #stats.defensa = int(sopa.select_one('span[class="bp3-tag p p-80"]').text.strip())
        stats.estabilidad = int(sopa.find('span', string='Strength').find_previous_sibling('em').text.strip())
        stats.resistencia = int(sopa.find('span', string='Stamina').find_previous_sibling('em').text.strip())
        stats.velMax = int(sopa.find('span', string='Sprint speed').find_previous_sibling('em').text.strip())
        stats.aceleracion = int(sopa.find('span', string='Acceleration').find_previous_sibling('em').text.strip())

        
        #stats.respuesta = int(sopa.find('span', string='Reactions').find_previous_sibling('em').text.strip())

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
        workRateTxt = (sopa.find('label', string='Work rate').find_parent("p").text.split(" ", 2)[-1].strip())        
        if workRateTxt == "Low/ Low":
            stats.estadoForma = 4
        elif workRateTxt == "Medium/ Low":
            stats.estadoForma = 5
        elif workRateTxt == "Medium/ Medium":
            stats.estadoForma = 6
        elif workRateTxt == "High/ Medium":
            stats.estadoForma = 7
        elif workRateTxt == "High/ High":
            stats.estadoForma = 8
        

        
        stats.frecPieMalo = math.ceil((int(sopa.find('label', string='Weak foot').find_parent("p").text.split(" ")[0].strip()))*(8/5))
        stats.precPieMalo = math.ceil((stats.frecPieMalo+stats.tecnica*(8/100))/2)
        
        stats.resistenciaLesion = math.ceil((stats.estabilidad+stats.resistencia)*(8/200))


        #tod = ul.find_all('em')
        #for x in todo:
        #    print(x.text)

        print(jugador.pie) 
                

        #nombre = sopa.select_one('h1[class="data-header__headline-wrapper"]').text.split("\n")[-1].strip()
        #fechaNacimiento = sopa.select_one('span[itemprop="birthDate"]').text.strip().split(" ")[0]
        #estatura = int(float(sopa.select_one('span[itemprop="height"]').text.strip().split(" ")[0].replace(",", ".")) * 100)
        #pie = True if sopa.find('span', string='Pie:').find_next('span').text.strip() == "ambidiestro" or "derecho" else False
        #estado = True if sopa.select_one('span[itemprop="affiliation"]').text.strip() != "Retirado" else False
        
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print(e.with_traceback())
    
recibirCodigo(192505, clases.Jugador(None, 1, "XSDDDD", 2, 2, 2 ,2 ,2, 2, 2))