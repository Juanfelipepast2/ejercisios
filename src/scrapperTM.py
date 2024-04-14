#TODO ENCONTRAR FOTO DE JUGADOR
import requests
from bs4 import BeautifulSoup

def recibirLink(link):
    try:
        headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

        resultado = requests.get(link, headers=headers)        
        
        
        sopa = BeautifulSoup(resultado.content, "html.parser")
        
        nombre = sopa.select_one('h1[class="data-header__headline-wrapper"]').text.split("\n")[-1].strip()
        fechaNacimiento = sopa.select_one('span[itemprop="birthDate"]').text.strip().split(" ")[0]
        estatura = int(float(sopa.select_one('span[itemprop="height"]').text.strip().split(" ")[0].replace(",", ".")) * 100)
        pie = sopa.find('span', string='Pie:').find_next('span').text.strip()
        estado = True if sopa.select_one('span[itemprop="affiliation"]').text.strip() != "Retirado" else False
        print(nombre)
        print(fechaNacimiento)
        print(estatura)
        print(pie)
        print(estado)
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print(e.with_traceback())
    
recibirLink("https://www.transfermarkt.co/ronaldo/profil/spieler/3140")
    