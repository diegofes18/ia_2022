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

"""
CLASE INDIVIDU:
    -__individu: cromosoma que representa el conjunt de gens que conté l'individu
    -la resta d'atributs representen les percepcions que rep
"""
class Individu:
    def __init__(self, posPizza, posAgent, parets, individu, valor=None):
        self.__pos_ag = posAgent
        self.__individu = individu
        self.__pos_pizza = posPizza
        self.__parets = parets

        self.__fitness = valor
        # self.aplica_mov("Miquel")

    def __eq__(self, other):
        return self.__fitness == other.get_valor()
    """"
    Funció per ordenar a la cua de prioritat segons la fitness de l'individu
    """
    def __lt__(self, other):
        return self.__fitness < other.get_valor()

    def get_valor(self):
        return self.__fitness

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

    """"
    FUNCIÓ DE CREUAMENT:
    Aquesta funció serveix per augmentar la població amb la generació de fills de dos bons individus
        - Per fer aixó agafam un punt de creuament aleatoria per a cada fill on s'agafará una part del pare i la resta 
        de la mare
        - Quan generam cada fill hem de recortar la part dels gens que pasen per una paret o fora i ens quedam amb els
        moviments (gens) válids, a la funció corta()
        -En el moment en que generam un individu fill hi ha una probabilitat de 50% de mutació, a la funció muta()
        - Per darrer aclarar que el número de fills es aleatòri
    """

    def crossover(self, mother):
        num_hijos = random.randint(0, len(self.__individu))
        hijos = []
        for i in range(num_hijos):
            cross_point = random.randint(0, len(self.__individu))
            sub_hijo1 = self.__individu[:cross_point]
            sub_hijo2 = mother.__individu[cross_point:]
            sub_hijo1.extend(sub_hijo2)
            indiv = Individu(self.__pos_pizza, self.__pos_ag, self.__parets, sub_hijo1)
            indiv.corta()
            # Probabilidad de mutación del 50%
            prob_mutacion = random.randint(0, 1)
            if prob_mutacion == 1:
                indiv.muta()
            hijos.append(indiv)
        return hijos
    """"
    La funció de mutació s'executa per un de cada dos fills generats.
    Hi ha dos tipus de mutacions amb la mateixa probabilitat:
        -Es pot afegir un gen al cromosoma, es a dir , s'afegeix un moviment al camí
        -L'altra opció es que es canvi un gen (moviment) dels ja presents a l'individu
    """
    def muta(self):
        movs = ((-1, 0), (+1, 0), (0, -1), (0, +1), (-2, 0), (+2, 0), (0, -2), (0, +2))
        tipo_mutacion = random.randint(0, 1)
        # Mutación de añadir un gen
        if tipo_mutacion == 0:
            self.__individu.append(movs[random.randint(0, 7)])
        # Mutación de cambiar un gen
        else:
            self.__individu[random.randint(0, len(self.__individu) - 1)] = movs[random.randint(0, 7)]
    """"
    FUNCIÓ DE FITNESS:Aquesta funció asigna un valor fitness a l'individu
    Aquest número simplement representa la distància final a la que es trobarà l'individu de la pizza després d'haber 
    aplicat els seus moviments
    """
    def calc_fitness(self):
        # distancia a la que llega
        suma = list((0, 0))
        dist = 0
        for e in self.__individu:
            suma[0] += e[0]
            suma[1] += e[1]

        # distancia a la pizza
        for i in range(2):
            dist += abs(self.__pos_pizza[i] - suma[i])

        self.__fitness = dist

    def es_meta(self, string: str):
        return self.__fitness == 0

    def get_pos_pizza(self):
        return self.__pos_pizza

    """"
    Funció per a generar la població inicial.
    - S'assigna un camí aleatori a cada individu generat 
    - El numero d'individus de la població inicial sirà init
    -Tots es corten per a no descartar cap individu
    """
    def genera_init(self, init: int, string: str):
        poblacion_init = []
        movs = ((-1, 0), (+1, 0), (0, -1), (0, +1), (-2, 0), (+2, 0), (0, -2), (0, +2))
        for i in range(init):
            long_cam = random.randint(0, 20)
            camino = []
            camino.append(self.__pos_ag[string])
            for j in range(long_cam):
                camino.append(movs[random.randint(0, 7)])

            indiv = Individu(self.__pos_pizza, self.__pos_ag, self.__parets, camino)
            indiv.corta()
            poblacion_init.append(indiv)
        return poblacion_init

    def is_bad(self, suma):
        for x in self.__parets:
            if (suma[0] == x[0]) and (suma[1] == x[1]):
                return True
        if not ((suma[0] <= 7) and (suma[0] >= 0) and (suma[1] <= 7) and (suma[1] >= 0)):
            return True
        return False

    def corta(self):
        aux = []
        suma = []
        suma.append(0)
        suma.append(0)
        suma = list(suma)
        for e in self.__individu:
            suma[0] += e[0]
            suma[1] += e[1]

            if self.is_bad(suma):
                break
            aux.append(e)

        self.__individu = aux

    #Retornam una llista amb les accions, a partir dels gens de l'individu
    def set_accions(self, string):
        accions = []
        reversed = self.__individu[::-1]
        for gen in reversed:
            if not (gen == self.__pos_ag[string]):
                if gen == (0, 1):
                    accions.append((AccionsRana.MOURE, Direccio.BAIX))
                if gen == (1, 0):
                    accions.append((AccionsRana.MOURE, Direccio.DRETA))
                if gen == (0, -1):
                    accions.append((AccionsRana.MOURE, Direccio.DALT))
                if gen == (-1, 0):
                    accions.append((AccionsRana.MOURE, Direccio.ESQUERRE))
                if gen == (0, 2):
                    accions.append((AccionsRana.BOTAR, Direccio.BAIX))
                if gen == (0, -2):
                    accions.append((AccionsRana.BOTAR, Direccio.DALT))
                if gen == (2, 0):
                    accions.append((AccionsRana.BOTAR, Direccio.DRETA))
                if gen == (-2, 0):
                    accions.append((AccionsRana.BOTAR, Direccio.ESQUERRE))
        return accions


class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)

        self.__accions = None
        self.__torn = 0

    def pinta(self, display):
        pass
    #Funció per a la cerca de l'individu correcte
    def cerca_Genetic(self, estat: Individu, string: str):
        #Població aleatoria inicial
        poblacion = estat.genera_init(20, string)
        cola = PriorityQueue()
        #Ficam els individua a la cua de prioritat
        for p in poblacion:
            p.calc_fitness()
            cola.put(p)

        while len(poblacion) > 0:
            #Reproducimos por parejas los mejores de la cola de prioridad
            for i in range(10):
                padre = cola.get()
                madre = cola.get()
                #Aumentamos la poblacion con los hijos de la pareja
                poblacion.extend((padre.crossover(madre)))
                #Metemos en la cola la nueva población
                for p in poblacion:
                    p.calc_fitness()
                    cola.put(p)
                #Comprobamos si alguno es meta
                for i in range(cola.qsize()):
                    p = (list(cola.queue)[i])
                    if p.es_meta(string):
                        self.__accions = p.set_accions(string)
                        return True

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:

        percepciones = percep.to_dict()
        key = list(percepciones.keys())
        indiv = []
        indiv.append(percep[key[1]]["Miquel"])
        state = Individu(percep[key[0]], percep[key[1]], percep[key[2]], indiv)

        if self.__accions is None:
            self.cerca_Genetic(estat=state, string='Miquel')

        if self.__accions:
            if (self.__torn > 0):
                self.__torn -= 1
                return AccionsRana.ESPERAR
            else:
                acc = self.__accions.pop()
                print("accion:" + str(acc))
                if (acc[0] == AccionsRana.BOTAR):
                    self.__torn = 2
                # retornam acció i direcció
                return acc[0], acc[1]
        else:
            print("espera")
            return AccionsRana.ESPERAR
