#TODO ENCONTRAR FOTO DE JUGADOR
import requests
import clases
from bs4 import BeautifulSoup

def recibirLink(link, idPais: int):
    try:
        headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

        resultado = requests.get(link, headers=headers)        
        
        
        sopa = BeautifulSoup(resultado.content, "html.parser")
        
        nombre = sopa.select_one('h1[class="data-header__headline-wrapper"]').text.split("\n")[-1].strip()
        fechaNacimiento = sopa.select_one('span[itemprop="birthDate"]').text.strip().split(" ")[0]
        estatura = int(float(sopa.select_one('span[itemprop="height"]').text.strip().split(" ")[0].replace(",", ".")) * 100)
        pie = True if sopa.find('span', string='Pie:').find_next('span').text.strip() == "ambidiestro" or "derecho" else False
        estado = True if sopa.select_one('span[itemprop="affiliation"]').text.strip() != "Retirado" else False
        print(nombre)
        print(fechaNacimiento)
        print(estatura)
        print(pie)
        print(estado)
        
        jugador = clases.Jugador(None, idPais, nombre, fechaNacimiento, link, pie, estatura, None, estado, None)
        print(jugador)
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print(e.with_traceback())
    
recibirLink("https://www.transfermarkt.co/thomas-muller/profil/spieler/58358", 2)
    