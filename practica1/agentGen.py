
"""
CONSTANTS PER MOURE I ELS REUS COSTOS
"""
COST_DESPL = 1
COST_ESPERAR = 0.5
COST_BOTAR = 6

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import ClauPercepcio, AccionsRana, Direccio
from queue import PriorityQueue
import random

class Estat:
    def __init__(self,posPizza,posAgent,parets,individu,pes=0,pare=None, valor=None):
        self.__pos_ag = posAgent
        self.__individu = individu
        self.__pos_pizza = posPizza
        self.__parets = parets
        self.__pes = pes
        self.__pare = pare
        self.__valor = valor
        print(self.__individu)
        #self.aplica_mov("Miquel")

    def __eq__(self, other):
        return self.__valor == other.get_valor()
    def __lt__(self, other):
        return self.__valor < other.get_valor()
    def get_valor(self):
        return self.__valor
    def get_camino(self):
        return self.__individu

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

    def calc_fitness(self, string:str):
        #distancia a la que llega

        suma = list((0,0))

        dist = 0
        for e in self.__individu:

            suma[0] += e[0]
            suma[1] += e[1]
            #print(suma)
            for x in self.__parets:
                if (suma[0] == x[0]) and (suma[1] == x[1]):
                    dist += 1000
            if not ( (suma[0] <= 7) and (suma[0] >= 0) and (suma[1] <= 7) and (suma[1] >= 0) ):
                dist += 1000

        #distancia a la pizza

        for i in range(2):
            dist += abs(self.__pos_pizza[i] - suma[i])

        self.__valor=dist

    def crossover(self, other):
        print("padre cam:" + str(self.get_camino()))
        print("madre cam:" + str(other.get_camino()))
        cross_point = random.randint(0, len(self.__individu))
        sub_hijo1 = self.__individu[:cross_point]
        sub_hijo2 = other.cami[cross_point:]
        sub_hijo1.extend(sub_hijo2)

        hijos = []

        movs = {"ESQUERRE": (-1, 0), "DRETA": (+1, 0), "DALT": (0, -1), "BAIX": (0, +1)}
        claus = list(movs.keys())
        for i, m in enumerate(movs.values()):
            h = []
            h = sub_hijo1.copy()
            h.append(m)
            hijos.append(Estat(self.__pos_pizza, self.__pos_ag, self.__parets, h,
                                        pare=(self, (AccionsRana.MOURE, Direccio.__getitem__(claus[i])))))

        movs = {"ESQUERRE": (-2, 0), "DRETA": (+2, 0), "DALT": (0, -2), "BAIX": (0, +2)}
        claus = list(movs.keys())
        for i, m in enumerate(movs.values()):
            h = []
            h = sub_hijo1.copy()
            h.append(m)
            hijos.append(Estat(self.__pos_pizza, self.__pos_ag, self.__parets, h,
                               pare=(self, (AccionsRana.BOTAR, Direccio.__getitem__(claus[i])))))

        return hijos

    def crossover2(self, other):
        print("padre cam:" + str(self.get_camino()))
        print("madre cam:" + str(other.get_camino()))

        hijos = []

        movs = {"ESQUERRE": (-1, 0), "DRETA": (+1, 0), "DALT": (0, -1), "BAIX": (0, +1)}
        claus = list(movs.keys())
        for i, m in enumerate(movs.values()):
            cross_point = random.randint(0, len(self.__individu))
            sub_hijo1 = self.__individu[:cross_point]
            sub_hijo2 = other.cami[cross_point:]
            sub_hijo1.extend(sub_hijo2)

            h = []
            h = sub_hijo1.copy()
            h.append(m)
            hijos.append(Estat(self.__pos_pizza, self.__pos_ag, self.__parets, h,
                                        pare=(self, (AccionsRana.MOURE, Direccio.__getitem__(claus[i])))))

        movs = {"ESQUERRE": (-2, 0), "DRETA": (+2, 0), "DALT": (0, -2), "BAIX": (0, +2)}
        claus = list(movs.keys())
        for i, m in enumerate(movs.values()):
            cross_point = random.randint(0, len(self.__individu))
            sub_hijo1 = self.__individu[:cross_point]
            sub_hijo2 = other.cami[cross_point:]
            sub_hijo1.extend(sub_hijo2)

            h = []
            h = sub_hijo1.copy()
            h.append(m)
            hijos.append(Estat(self.__pos_pizza, self.__pos_ag, self.__parets, h,
                               pare=(self, (AccionsRana.BOTAR, Direccio.__getitem__(claus[i])))))

        return hijos

    def calcula_heuristica(self,string: str):
        sum=0
        for i in range(2):
            sum+=abs(self.__pos_pizza[i] - self.__pos_ag[string][i])
        return self.__pes+sum

    def es_valid(self,string: str):
        #claus = list(self.__pos_ag.keys())
        # mirar si hi ha parets
        for x in self.__parets:
            if (self.__pos_ag[string][0] == x[0]) and (self.__pos_ag[string][1] == x[1]):
                return False

        return (self.__pos_ag[string][0] <= 7) and (self.__pos_ag[string][0] >= 0) \
               and (self.__pos_ag[string][1] <= 7) and (self.__pos_ag[string][1] >= 0)

    def es_meta(self,string: str):
        return self.__valor==0

    def get_pos_pizza(self):
        return self.__pos_pizza

    def genera_init(self):

        poblacion_init = []

        movs = {"ESQUERRE": (-1, 0), "DRETA": (+1, 0), "DALT": (0, -1), "BAIX": (0, +1)}
        claus = list(movs.keys())
        for i,m in enumerate(movs.values()):
            h = []
            h.append(self.__individu[0])
            h.append(m)
            poblacion_init.append(Estat(self.__pos_pizza, self.__pos_ag, self.__parets,h,
                       pare=(self, (AccionsRana.MOURE, Direccio.__getitem__(claus[i])))) )

        movs = {"ESQUERRE": (-2, 0), "DRETA": (+2, 0), "DALT": (0, -2), "BAIX": (0, +2)}
        claus = list(movs.keys())
        for i, m in enumerate(movs.values()):
            h = []
            h.append(self.__individu[0])
            h.append(m)
            poblacion_init.append(Estat(self.__pos_pizza, self.__pos_ag, self.__parets, h,
                                   pare=(self, (AccionsRana.BOTAR, Direccio.__getitem__(claus[i])))))

        return poblacion_init


class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)

        self.__accions = None
        self.__torn = 0

    def pinta(self, display):
        pass



    def cerca_Genetic(self, estat: Estat, string:str):
        poblacion = estat.genera_init()
        cola = PriorityQueue()
        print("posicion pizza"+str(estat.get_pos_pizza()))
        #print(poblacion)
        while len(poblacion)>0:

            for p in poblacion:
                #print(p)
                p.calc_fitness(string)
                print(str(p)+" valor:"+str(p.get_valor())+", su camino"+str(p.get_camino()))
                if(p.get_valor()<1000):
                    cola.put(p)

            #enseñamos la cola
            for i in range(cola.qsize()):
                print(list(cola.queue)[i])

            padre = cola.get()
            cola.put(padre)
            print(str(padre) + " valor padre:" + str(padre.get_valor()))
            #print(puntuaciones)
            madre = cola.get()
            cola.put(madre)
            print(str(madre) + " valor madre:" + str(madre.get_valor()))
            poblacion=(padre.crossover2(madre))
            for p in poblacion:
                p.calc_fitness(string)
                print(str(p) + " valor:" + str(p.get_valor()) + ", su camino" + str(p.get_camino()))
                if (p.get_valor() < 1000):
                    cola.put(p)

            for i in range(cola.qsize()):
                p = (list(cola.queue)[i])
                if p.es_meta(string):
                    accions = []
                    iterador = p

                    while iterador.pare is not None:
                        pare, accio = iterador.pare

                        accions.append(accio)
                        iterador = pare
                    self.__accions = accions
                    return True



    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:

            percepciones = percep.to_dict()
            key = list(percepciones.keys())
            indiv = []
            indiv.append(percep[key[1]][self.nom])
            state = Estat(percep[key[0]],percep[key[1]], percep[key[2]],indiv)

            if self.__accions is None:
                self.cerca_Genetic(estat=state,string='Miquel')

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