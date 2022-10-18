""" Mòdul que conté l'agent per jugar al joc de les monedes.

Percepcions:
    ClauPercepcio.MONEDES
Solució:
    " XXXC"
"""

from ia_2022 import agent, entorn
from monedes.entorn import ClauPercepcio, AccionsMoneda
from queue import PriorityQueue
from monedes.joc import Moneda

SOLUCIO = " XXXC"

class Estat():


    def __init__(self, pare=None):
        self.__pare = pare
        self.__monedas = Moneda


        def get_pare(self):
            return self.__pare
        def set_pare(self, value):
            self.__pare = value

        def genera_fill(self) -> dict:
            # numero entero
            costs = dict()
            for act in AccionsMoneda:
                estatf_i = Estat()
                cost = act.value
                estatf_i = Moneda._aplica(act)



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

        self.__oberts.put(3, estat)
        actual = None
        while not self.__oberts.empty():
            actual = self.__oberts.get()
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
                pass
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
        pass
