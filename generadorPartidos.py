from calendar import c
from src.clases import Equipo
from src.clases import Partido







def crearLiga():
    equipos = []
    for i in range(0, 8):
        #equipos.append(("Equipo " + str(chr(97+i)), i))
        equipos.append(Equipo(nombre="Equipo " + str(chr(97+i)), id=i, idReset=None, idTecnico=None, presupuesto=0, escudo=None))
    return equipos


def fixtures(teams):
    if len(teams) % 2:
        teams.append(Equipo(nombre='Descansa', idTecnico=len(teams)))  # if team number is odd - use 'day off' as fake team     
    contadores = [[0,0]]* len(teams)

    rotation = list(teams)       # copy the list

    fixtures = []
    for i in range(0, len(teams)-1):        
        fechaTemp = []
        for j in range(0, int(len(teams)/2)):
            #if (rotation[j].nombre != 'Descansa' and rotation[len(teams)-1-j].nombre != 'Descansa'):
            if j == 7:
                print("hola")
            if i % 2 == 0:
                fechaTemp.append(Partido(equipoLocal=rotation[j], equipoVisitante=rotation[len(teams)-1-j]))
                contadores[j] = [contadores[j][0] + 1, contadores[j][1]]
                contadores[len(teams)-1-j] = [contadores[len(teams)-1-j][0], contadores[len(teams)-1-j][1] + 1]

            else:
                fechaTemp.append(Partido(equipoLocal=rotation[len(teams)-1-j], equipoVisitante= rotation[j]))
                contadores[len(teams)-1-j] = [contadores[len(teams)-1-j][0] + 1, contadores[len(teams)-1-j][1]]
                contadores[j] = [contadores[j][0], contadores[j][1] + 1]

        
        fixtures.append(fechaTemp)
        rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]

    return fixtures

arrayEquipos = crearLiga()
arrayPartidos = fixtures(arrayEquipos)

for i in range(0, len(arrayPartidos)):
    print("Jornada " + str(i + 1))
    for x in arrayPartidos[i]:        
        print(x.equipoLocal.nombre + " vs " + x.equipoVisitante.nombre)
    print("\n")