
"""
CONSTANTS PER MOURE I ELS REUS COSTOS
"""
"""
COST_DESPL = 1
COST_ESPERAR = 0.5
COST_BOTAR = 6
"""

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import ClauPercepcio, AccionsRana, Direccio

class Estat:
    def __init__(self,posPizza,posAgent,parets, nom_Max, puntuacio=0,pare=None):
        self.__pos_ag = posAgent
        self.__nom_max = nom_Max
        self.__pos_pizza = posPizza
        self.__parets = parets
        self.__puntuacio = puntuacio
        self.__pare = pare

    def __eq__(self, other):
        return self.__pos_ag == other.get_pos_ag()
    def __lt__(self, other):
        return False
    def __hash__(self):
        return hash(tuple(self.__pos_ag))

    def get_pos_ag(self):
        return self.__pos_ag
    def get_othername(self):
        claves = list(self.__pos_ag.keys())
        if self.__nom_max == claves[0]:
            return claves[1]
        else:
            return claves[0]

    @property
    def pare(self):
        return self.__pare
    def get_pos_ag2(self):
        return list(self.__pos_ag.keys())[1]
    @pare.setter
    def pare(self, value):
        self.__pare = value

    def point(self, clave):
        sum1 = 0
        for i in range(2):
            sum1 += abs(self.__pos_pizza[i] - self.__pos_ag[clave][i])

        return sum1

    def calcula_puntuacio(self):

        claves = list(self.__pos_ag.keys())

        if self.__nom_max == claves[0]:
            return self.point(claves[1])-self.point(claves[0])
        else:
            return self.point(claves[0])-self.point(claves[1])


    def es_valid(self):
        # mirar si hi ha parets

        for x in self.__parets:

            if (self.__pos_ag[self.get_othername()][0] == x[0]) and (self.__pos_ag[self.get_othername()][1] == x[1]):
                return False

        return (self.__pos_ag[self.get_othername()][0] <= 7) and (self.__pos_ag[self.get_othername()][0] >= 0) \
               and (self.__pos_ag[self.get_othername()][1] <= 7) and (self.__pos_ag[self.get_othername()][1] >= 0)

    def es_meta(self):
        return (self.__pos_ag[self.get_othername()][0] == self.__pos_pizza[0])and(self.__pos_ag[self.get_othername()][1] == self.__pos_pizza[1])

    def get_pos_pizza(self):
        return self.__pos_pizza

    def genera_fills(self):
        claves = list(self.__pos_ag.keys())
        if self.__nom_max == claves[0]:
            nom_rana = claves[1]
        else:
            nom_rana = claves[0]
        print("nom max:    "+str(self.__nom_max)+" ->posicion: "+str(self.__pos_ag))
        fills = []
        movs={"ESQUERRE":(-1,0),"DRETA":(+1,0), "DALT": (0,-1), "BAIX": (0,+1)}
        claus=list(movs.keys())
        for i, m in enumerate(movs.values()):
            coords = [sum(tup) for tup in zip(self.__pos_ag[self.__nom_max], m)]
            #coord = {self.__nom_max: coords}
            self.__pos_ag[self.__nom_max]=coords
            print(self.__pos_ag)
            print(m)
            actual = Estat(self.__pos_pizza, self.__pos_ag, self.__parets, nom_rana, 0,
                           (self, (AccionsRana.MOURE, Direccio.__getitem__(claus[i]))))
            if (actual.es_valid()):
                fills.append(actual)


        movs = {"ESQUERRE": (-2,0),"DRETA": (+2,0), "DALT": (0,-2), "BAIX": (0,+2)}
        claus = list(movs.keys())
        for i, m in enumerate(movs.values()):
            print(m)
            coords = [sum(tup) for tup in zip(self.__pos_ag[self.__nom_max], m)]
            coord = {self.__nom_max: coords}
            self.__pos_ag[self.__nom_max]=coords
            print(self.__pos_ag)
            actual = Estat(self.__pos_pizza, self.__pos_ag, self.__parets, nom_rana, 0,
                           (self, (AccionsRana.BOTAR, Direccio.__getitem__(claus[i]))))
            if (actual.es_valid()):
                fills.append(actual)

        return fills



class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__accions = None
        self.__torn = 0

    def pinta(self, display):
        pass

    def minimax(self, estat:Estat, turno_max: bool, recurs: int):

        score = estat.calcula_puntuacio()
        if recurs == 5 or estat.es_meta():
            return score, estat
        #[print(self.minimax(estat_fill, not turno_max, recurs + 1)) for estat_fill in estat.genera_fills()]
        point_fills = [self.minimax(estat_fill, not turno_max, recurs+1) for estat_fill in estat.genera_fills()]
        punto = point_fills
        #print(punto)
        if turno_max:
            return max(punto)
        else:
            return min(punto)

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:

            percepciones = percep.to_dict()
            key = list(percepciones.keys())
            inicia = (list(percep[key[1]].keys())[0])
            state = Estat(percep[key[0]], percep[key[1]], percep[key[2]], inicia)


            #if self.__accions is None:

            now = self.minimax(estat=state, turno_max=True, recurs=0)
            print("hola")

            accions = []
            iterador = now[1]

            while iterador.pare is not None:
                pare, accio = iterador.pare

                accions.append(accio)
                iterador = pare
            self.__accions = accions

            if self.__accions:
                if(self.__torn>0):
                    self.__torn-=1
                    return AccionsRana.ESPERAR
                else:
                    acc=self.__accions.pop()
                    print("accion:"+str(acc))
                    if(acc[0]==AccionsRana.BOTAR):
                        self.__torn=2
                    #retornam acció i direcció
                    return acc[0],acc[1]
            else:
                return AccionsRana.ESPERAR