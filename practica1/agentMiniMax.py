
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
from queue import PriorityQueue

class Estat:
    def __init__(self,posPizza,posAgent,parets,puntuacio=0,pare=None):
        self.__pos_ag = posAgent
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

    @property
    def pare(self):
        return self.__pare

    @pare.setter
    def pare(self, value):
        self.__pare = value

    def point(self, string: str):
        return ClauPercepcio[string].OLOR

    def calcula_puntuacio(self,string: str):
        if string == 'Miquel':
            return self.point('Diego') - self.point('Miquel')
        else:
            return self.point('Miquel') - self.point('Diego')


    def es_valid(self,string: str):
        # mirar si hi ha parets
        for x in self.__parets:
            if (self.__pos_ag[string][0] == x[0]) and (self.__pos_ag[string][1] == x[1]):
                return False

        return (self.__pos_ag[string][0] <= 7) and (self.__pos_ag[string][0] >= 0) \
               and (self.__pos_ag[string][1] <= 7) and (self.__pos_ag[string][1] >= 0)

    def es_meta(self,string: str):
        return (self.__pos_ag[string][0] == self.__pos_pizza[0])and(self.__pos_ag[string][1] == self.__pos_pizza[1])

    def get_pos_pizza(self):
        return self.__pos_pizza

    def genera_fills(self,string: str):
        fills = []
        movs={"ESQUERRE":(-1,0),"DRETA":(+1,0), "DALT": (0,-1), "BAIX": (0,+1)}
        claus=list(movs.keys())
        for i, m in enumerate(movs.values()):
            coords = [sum(tup) for tup in zip(self.__pos_ag[string], m)]
            coord = {string: coords}
            actual = Estat(self.__pos_pizza, coord, self.__parets, 0,
                           (self, (AccionsRana.MOURE, Direccio.__getitem__(claus[i]))))
            if (actual.es_valid(string)):
                fills.append(actual)


        movs = {"ESQUERRE": (-2,0),"DRETA": (+2,0), "DALT": (0,-2), "BAIX": (0,+2)}
        claus = list(movs.keys())
        for i, m in enumerate(movs.values()):
            coords = [sum(tup) for tup in zip(self.__pos_ag[string], m)]
            coord = {string: coords}
            actual = Estat(self.__pos_pizza, coord, self.__parets, 0,
                           (self, (AccionsRana.BOTAR, Direccio.__getitem__(claus[i]))))
            if (actual.es_valid(string)):
                fills.append(actual)

        return fills



class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__tancats = None
        self.__oberts = None
        self.__accions = None
        self.__torn = 0

    def pinta(self, display):
        pass

    def minimax(self, estat:Estat, turno_max: bool, recurs: int):

        if self.nom == 'Miquel':
            nom_rana = 'Miquel'
        else:
            nom_rana = 'Diego'

        score = estat.calcula_puntuacio(nom_rana)
        if recurs == 5 or estat.es_meta(nom_rana):
            return score, estat

        point_fills = [self.minimax(estat_fill, not turno_max, recurs+1) for estat_fill in estat.genera_fills(nom_rana)]

        if turno_max:
            return max(point_fills),estat
        else:
            return min(point_fills),estat

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:

            percepciones = percep.to_dict()
            key = list(percepciones.keys())
            state = Estat(percep[key[0]],percep[key[1]], percep[key[2]])

            if self.__accions is None:
                self.minimax(estat=state, turno_max=True, recurs=0)

            accions = []
            iterador = state

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