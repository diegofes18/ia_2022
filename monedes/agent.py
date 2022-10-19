""" Mòdul que conté l'agent per jugar al joc de les monedes.

Percepcions:
    ClauPercepcio.MONEDES
Solució:
    " XXXC"
"""

from ia_2022 import agent, entorn
from monedes.entorn import ClauPercepcio, AccionsMoneda
from queue import PriorityQueue


SOLUCIO = " XXXC"

class Estat:
    def __init__(self,info,pes=0,pare=None):

        if(info is not None):
            self.__info=info
        else:
            self.__info={}
        self.__pare=pare
        self.__pes=pes

    def get_weight(self):
        return self.__pes
    def set_weight(self, pes):
        self.__pes = pes

    def get_heuristica(self):
        clau = list(self.__info.keys())  # llista claus
        h=self.__info[clau[0]].index(' ')
        for i in range(len(self.__info[clau[0]])):
            print("I: "+str(i))
            if(self.__info[clau[0]][i] != SOLUCIO[i])and(self.__info[clau[0]][i] != ' '):
                h+=1

        return h + self.__pes

    def genera_fills(self) -> list:
        clau = list(self.__info.keys())
        llista = [*self.__info[clau[0]]]  # string to list
        for elem in llista:
            for act in AccionsMoneda:
                estat_fi = Estat()



    def es_meta(self) -> bool:
        clau = list(self.__info.keys())
        if (clau == SOLUCIO):
            return True
        else:
            return False





class AgentMoneda(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=0)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def pinta(self, display):
        print(self._posicio_pintar)

    def _cerca(self, estat: Estat):
        self.__oberts = PriorityQueue()
        self.__tancats = set()

        self.__oberts.put((0, estat))
        actual = None
        while self.__oberts.qsize() > 0:
            actual = self.__oberts.get()[1]
            print(str(actual))
            #self.__oberts = self.__oberts[1:]
            if actual in self.__tancats:
                continue

            #if not actual.es_segur():
            #    self.__tancats.add(actual)
            #    continue

            estats_fills = actual.genera_fill()

            if actual.es_meta():
                break

            for estat_f in estats_fills:
                self.__oberts.put((estat_f.get_weight(), estat_f))
                #self.__oberts.append(estat_f)

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


    def calculate_f(self, estatf:Estat, estatp:Estat):
        pass

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        estat = Estat(percep.to_dict())

        if self.__accions is None:
            self._cerca(estat=estat)

        if len(self.__accions) > 0:
            return self.__accions.pop()
        else:
            return 3  # res
        pass
