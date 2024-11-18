from calendar import c
from src.clases import Equipo
from src.clases import Partido

def crearLiga():
    equipos = []
    for i in range(0,9):
        #equipos.append(("Equipo " + str(chr(97+i)), i))
        equipos.append(Equipo(nombre="Equipo " + str(chr(97+i)), id=i, idReset=None, idTecnico=None, presupuesto=0, escudo=None))
    return equipos

def fixtures(teams):    
    paresFlag = True

    if len(teams) % 2 != 0:
        teams.insert(0,Equipo(nombre='Descansa', idTecnico=len(teams)))  # if team number is odd - use 'day off' as fake team     
        paresFlag = False

    rotation = list(teams)       # copy the list
    fixtures = []

    for i in range(0, len(teams)-1):        
        fechaTemp = []

        for j in range(0, int(len(teams)/2)):
            if (paresFlag == True and i % 2 != 0 and rotation[j] == rotation[0]):                            
                anadirModificarPartido(fechaTemp, rotation[-1-j], rotation[j])                
            else:
                anadirModificarPartido(fechaTemp, rotation[j], rotation[-1-j])
    
        fixtures.append(fechaTemp)
        rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]

    return fixtures

def anadirModificarPartido(fecha, equipoA, equipoB): #''' True = añadir, False = modificar'''
   
    fecha.append(Partido(equipoLocal=equipoA, equipoVisitante=equipoB))        

    if (fecha[-1].equipoLocal.nombre == debugEquipo):
            contadorLocalias[0] += 1
    elif (fecha[-1].equipoVisitante.nombre == debugEquipo):
        contadorLocalias[1] +=1



def printPartidos():
    for i in range(0, len(arrayPartidos)):
        print("Jornada " + str(i + 1))

        for x in arrayPartidos[i]:        
            print(x.equipoLocal.nombre + " vs " + x.equipoVisitante.nombre)
            
        print("\n")

    print("Localias: " + str(contadorLocalias[0]) + " Visitantes: " + str(contadorLocalias[1]) + "\n")

contadorLocalias = [0, 0]
debugEquipo = "Equipo i"
arrayEquipos = crearLiga()
arrayPartidos = fixtures(arrayEquipos)
printPartidos()