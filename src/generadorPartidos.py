

class Equipo:
    def __init__(self, nombre, posicion):
        self.nombre = nombre
        self.posicion = posicion

    def __str__(self):
        return str(self.posicion + 1) + "\t" + self.nombre + " " 

   
class Partido:
    def __init__(self, equipo1, equipo2):
        self.equipo1 = equipo1
        self.equipo2 = equipo2

    def __str__(self):
        return self.equipo1.nombre + " vs " + self.equipo2.nombre
    


def crearLiga():
    equipos = []
    for i in range(0, 15):
        equipos.append(Equipo("Equipo " + str(chr(97+i)), i))
    return equipos


def fixtures(teams):
    if len(teams) % 2:
        teams.append(Equipo("Descansa", len(teams)))  # if team number is odd - use 'day off' as fake team     

    rotation = list(teams)       # copy the list

    fixtures = []
    for i in range(0, len(teams)-1):        
        fechaTemp = []
        for j in range(0, int(len(teams)/2)):
            if i % 2 == 0:
                fechaTemp.append(Partido(rotation[j], rotation[len(teams)-1-j]))
            else:
                fechaTemp.append(Partido(rotation[len(teams)-1-j], rotation[j]))
        fixtures.append(fechaTemp)
        rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]

    return fixtures

arrayEquipos = crearLiga()
arrayPartidos = fixtures(arrayEquipos)

for i in range(0, len(arrayPartidos)):
    print("Jornada " + str(i + 1))
    for x in arrayPartidos[i]:        
        print(x)
    print("\n")