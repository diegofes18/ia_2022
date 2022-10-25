
"""
CONSTANTS PER MOURE I ELS REUS COSTOS
"""
COST_DESPL=1
COST_ESPERAR=0.5
COST_BOTAR=6

from ia_2022 import entorn
from practica1 import joc
from entorn import *

COST_ESPERAR=0.5
COST_BOTAR=6
COST_DESPL=1
class Estat:
    def __init__(self,posAgent,posPizza,parets,pes,pare=None):
        self.__pos_ag = posAgent
        self.__pos_pizza = posPizza
        self.__parets = parets
        self.__pes = pes
        self.__pare = pare

    def getPosAg(self):
        return self.__pos_ag

    def calculaHeuristica(self):
        sum=0
        for i in range(2):
            sum+=abs(self.__pos_pizza[i] - self.__pos_ag[i])
        return self.__pes+sum

    def es_valid(self):
        if(0<=self.__pos_ag[0]<=7)and(0<=self.__pos_ag[1]<=7):
            return True
        else:
            return False

    def es_meta(self):
        return self.__pos_ag == self.__pos_pizza

    def getPosAg(self):
        return self.__pos_ag
    def getPosPizza(self):
        return self.__pos_pizza
    def generaFills(self):
        movs={"ESQUERRE":(0,-1),"DRETA":(0,+1),"DALT": (+1,0),"BAIX": (0,-1)}
        claus=movs.keys()
        fills=[]

        """
        Cas 1: Moviments de desplaçament a caselles adjacents.
        """
        for i,m in enumerate(movs.values()):
            pos = [sum(tup) for tup in zip(self.__pos_ag, m)]
            cost=self.calculaHeuristica()+COST_DESPL
            actual=Estat(pos, self.__pos_pizza, self.__parets, cost, (self, (AccionsRana.MOURE, Direccio.__getitem__(claus[i]))))
            if(actual.es_valid()):
                fills.append(actual)

        """
        Cas 2: Moviments de desplaçament de 2 caselles en caselles
        """
        movs = {"ESQUERRE": (0, -2), "DRETA": (0, +2), "DALT": (+2, 0), "BAIX": (0, -2)}
        for i,m in enumerate(movs.values()):
            pos = [sum(tup) for tup in zip(self.__pos_ag, m)]
            cost = self.calculaHeuristica() + COST_BOTAR
            actual = Estat(pos, self.__pos_pizza, self.__parets, cost,
                           (self, (AccionsRana.BOTAR, Direccio.__getitem__(claus[i]))))
            if (actual.es_valid()):
                fills.append(actual)

        return fills



class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__tancats = None
        self.__oberts = None
        self.__accions = None

    def pinta(self, display):
        pass

    def cerca_prof(self, estat:Estat):
        self.__oberts = []
        self.__tancats = dir()

        self.__oberts.append(estat)

        actual = None
        while len(self.__oberts) > 0:
            actual = self.__oberts.pop()
            if actual in self.__tancats:
                continue

            if not actual.es_valid():
                self.__tancats.add(actual)
                continue

            estats_fills = actual.genera_fill()

            if actual.es_meta():
                break

            for estat_f in estats_fills:
                self.__oberts.append(estat_f)

            self.__tancats.add(actual)
        if actual is None:
            raise ValueError("Error impossible")

        if actual.es_meta():
            accions = []
            iterador = actual

            while iterador.pare is not None:
                pare, accio = iterador.pare

                accions.append(accio)
                iterador = pare
            self.__accions = accions
            return True
        else:
            return False

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:

            estat = Estat(percep.to_dict(),posPizza=(3,1), parets=True, pes=0)


            self.cerca_prof(estat=estat)

            if len(self.__accions) > 0:
                return  AccionsRana.MOURE, self.__accions.pop()
            else:
                return AccionsRana.ESPERAR