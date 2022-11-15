
"""
CONSTANTS PER MOURE I ELS REUS COSTOS
"""
COST_DESPL = 1
COST_ESPERAR = 0.5
COST_BOTAR = 6


from practica1 import joc
from practica1.entorn import ClauPercepcio, AccionsRana, Direccio
from queue import PriorityQueue
import random

class Individu:
    def __init__(self,posPizza,posAgent,parets,individu, valor=None):
        self.__pos_ag = posAgent
        self.cami = individu
        self.__pos_pizza = posPizza
        self.__parets = parets
        self.__valor = valor
        #self.aplica_mov("Miquel")

    def __eq__(self, other):
        return self.__valor == other.get_valor()
    def __lt__(self, other):
        return self.__valor < other.get_valor()
    def get_valor(self):
        return self.__valor
    def get_camino(self):
        return self.cami

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

    def calc_fitness(self):
        #distancia a la que llega

        suma = list((0,0))

        dist = 0
        for e in self.cami:

            suma[0] += e[0]
            suma[1] += e[1]
        for i in range(2):
            dist += abs(self.__pos_pizza[i] - suma[i])

        self.__valor=dist

    def crossover(self, other):
        hijos = []
        return hijos

    def crossover2(self, other):


        hijos = []

        movs = {"ESQUERRE": (-1, 0), "DRETA": (+1, 0), "DALT": (0, -1), "BAIX": (0, +1)}
        claus = list(movs.keys())
        for i, m in enumerate(movs.values()):
            cross_point = random.randint(0, len(self.cami))
            sub_hijo1 = self.cami[:cross_point]
            sub_hijo2 = other.cami[cross_point:]
            sub_hijo1.extend(sub_hijo2)

            h = []
            h = sub_hijo1.copy()

            h.append(m)
            actual=Individu(self.__pos_pizza, self.__pos_ag, self.__parets, h,
                            (self, (AccionsRana.MOURE, Direccio.__getitem__(claus[i]))))
            if(actual.es_valid('Miquel')):
                hijos.append(actual)

        movs = {"ESQUERRE": (-2, 0), "DRETA": (+2, 0), "DALT": (0, -2), "BAIX": (0, +2)}
        claus = list(movs.keys())
        for i, m in enumerate(movs.values()):
            cross_point = random.randint(0, len(self.cami))
            sub_hijo1 = self.cami[:cross_point]
            sub_hijo2 = other.cami[cross_point:]
            sub_hijo1.extend(sub_hijo2)

            h = []
            h = sub_hijo1.copy()
            h.append(m)
            actual=Individu(self.__pos_pizza, self.__pos_ag, self.__parets, h,
                            (self, (AccionsRana.BOTAR, Direccio.__getitem__(claus[i]))))
            if (actual.es_valid('Miquel')):
                hijos.append(actual)

        return hijos


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

    def get_pos_parets(self):
        return self.__parets

    def genera_init(self, init:int):
        poblacion_init = []
        movs =[(-1, 0),  (+1, 0),  (0, -1),  (0, +1),
                (-2, 0), (+2, 0), (0, -2),  (0, +2)]
        for i in range(init):
            long_cami = random.randint(0,10)
            camino = []
            for j in range(long_cami):
                camino = []
                camino.append(movs[random.randint(0,7)])
            p=Individu(self.__pos_ag, self.__parets,self.__pos_pizza, camino)
            p.corta()
            poblacion_init.append(p)
        return poblacion_init

    def corta(self):
        init=list((0,0))
        aux = []
        for i in self.cami:
            init[0] += i[0]
            init[1] += i[1]
            if self.is_bad(init):
                break
            aux.append(i)
        self.cami = aux

    def is_bad(self,pos):
        for x in self.__parets:
            if (pos[0] == x[0]) and (pos[1] == x[1]):
                return True
        if  not( (pos[0] <= 7) and (pos[0] >= 0) and (pos[1] <= 7) and (pos[1] >= 0) ):
            return True
        return False

    def set_accions(self,string):
        accions = []
        for gen in self.cami:
            if not(gen==self.__pos_ag[string]):
                if gen == (0,1):
                    accions.append((AccionsRana.MOURE, Direccio.BAIX))
                if gen == (1,0):
                    accions.append((AccionsRana.MOURE, Direccio.DRETA))
                if gen == (0,-1):
                    accions.append((AccionsRana.MOURE, Direccio.DALT))
                if gen == (-1,0):
                    accions.append((AccionsRana.MOURE, Direccio.ESQUERRE))
                if gen == (0,2):
                    accions.append((AccionsRana.BOTAR, Direccio.BAIX))
                if gen == (0,-2):
                    accions.append((AccionsRana.BOTAR, Direccio.DALT))
                if gen == (2,0):
                    accions.append((AccionsRana.BOTAR, Direccio.DRETA))
                if gen == (-2,0):
                    accions.append((AccionsRana.BOTAR, Direccio.ESQUERRE))
        return accions



class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)

        self.__accions = None
        self.__torn = 0

    def pinta(self, display):
        pass


    def cerca_Genetic(self, estat: Individu, string:str):
        poblacion = estat.genera_init(10)
        cola = PriorityQueue()
        #print(poblacion)

        for p in estat.genera_init(10):
            # print(p)
            p.calc_fitness()
            if (p.get_valor() < 1000):
                cola.put(p)

        while len(poblacion)>0:

            #enseñamos la cola

            padre = cola.get()

            #print(puntuaciones)
            madre = cola.get()
            #cola.put(madre)
            #cola.put(padre)
            poblacion=(padre.crossover2(madre))
            for p in poblacion:
                p.calc_fitness(string)
                if (p.get_valor() < 1000):
                    cola.put(p)

            for i in range(cola.qsize()):
                p = (list(cola.queue)[i])
                if p.es_meta(string):
                    print(str(p) + " valor:" + str(p.get_valor()) + ", su camino" + str(p.get_camino()))
                    self.__accions=p.set_accions(string)
                    return True

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:

            percepciones = percep.to_dict()
            key = list(percepciones.keys())
            indiv = []
            indiv.append(percep[key[1]][self.nom])
            state = Individu(percep[key[0]], percep[key[1]], percep[key[2]], indiv)

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
                print("espera")
                return AccionsRana.ESPERAR
