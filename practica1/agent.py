"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from ia_2022 import entorn
from practica1 import joc


class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def pinta(self, display):
        print(self._posicio_pintar)

    def cerca_no_info(self, estat_inicial):
        pass

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        pass


class Estat:
    def __init__(self, pes: int, agent, pizza, parets, pare:None):
        self.__pare = pare
        self.__pes = pes
        self.__pos_agent = agent
        self.__pos_pizza = pizza
        self.__parets = parets

    def __hash__(self):
        return hash(tuple(self.__pos_agent))

    @property
    def pos_agent(self):
        return self.__pos_agent

    def es_meta(self) -> bool:
        return self.__pos_agent == self.__pos_pizza

    def calc_heuristica(self) -> int:
        x = abs(self.__pos_agent[0]-self.__pos_pizza[0])
        y = abs(self.__pos_agent[1]-self.__pos_pizza[1])
        return (x+y)+self.__pes

    def genera_fills(self):
        fills = []

