#!/usr/bin/python3
import random
import math

from campionatore_gibbs import CampionatoreDiGibbs

class GeneratoreColorazioneGrafo:

    def __init__(self, grafo, epsilon=0.1):
        """
        Inizializza la classe ColorazioneGrafo.

        :param grafo: Un dizionario che rappresenta il grafo, dove le chiavi sono i nodi e i valori sono liste di nodi adiacenti.
        :param q: Il numero di colori disponibili.
        :param n: Il numero di iterazioni per la colorazione.
        """
        self.grafo = grafo
        self.d = self.calcola_grado_max()
        self.q = 2 * (self.d ** 2) + 1  # Assicuriamoci che q > 2(d^2)
        # self.epsilon = epsilon  # Epsilon è un valore positivo

        self.k = len(grafo)  # Numero di nodi nel grafo
        # self.n = self.calcola_n()  # Calcola n in base a epsilon

        self.n = 100
        self.epsilon = self.calcola_epsilon()  # Calcola epsilon in base al grado massimo del grafico

        print(f"GeneratoreColorazioneGrafo inizializzato con q={self.q}, epsilon={self.epsilon}, n={self.n}, k={self.k}, d={self.d}")



    def calcola_grado_max(self):
        """
        Calcola il grado massimo del grafo.

        :param grafo: Un dizionario che rappresenta il grafo.
        :return: Il grado massimo.
        """
        return max(len(adiacenti) for adiacenti in self.grafo.values())

    def calcola_n(self):
        """
        Calcola n intero approssimato per eccesso.

        :param k: Un numero intero.
        :param epsilon: Un valore positivo.
        :param d: Un numero intero positivo (grado).
        :param q: Un numero intero positivo (numero di colori).
        :return: Un intero n che soddisfa l'inequazione.
        """
        # Calcola il logaritmo
        log_k = math.log(len(self.grafo))  # Calcola il logaritmo in base 2 della lunghezza del grafo
        log_epsilon = math.log(self.epsilon)
        log_d = math.log(self.d)
        log_q_over_2d2 = math.log(self.q / (2 * self.d**2))

        # Calcola l'espressione
        espressione = self.k * (1 + ((log_k - log_epsilon - log_d) / log_q_over_2d2))

        print(f"Logaritmi: log_k={log_k}, log_epsilon={log_epsilon}, log_d={log_d}, log_q_over_2d2={log_q_over_2d2}")
        # Arrotonda per eccesso
        n = math.ceil(espressione)
        print(f"Epsilon: {self.epsilon}, N calcolato: {n}")

        return n

    def calcola_epsilon(self):
        """
        Calcola epsilon in base al grado massimo del grafo.

        :return: Un valore epsilon calcolato.
        """
        # Calcola epsilon come 1 / (2 * d^2)
        epsilon = (self.k / (self.d * (self.q/(2 * self.d**2))**((self.n - self.k) / self.k)))  # Assicurati che q > 2(d^2)
        print(f"Epsilon calcolato: {epsilon}")
        return epsilon

    def get_n(self):
        """
        Restituisce il numero di iterazioni n.

        :return: Il numero di iterazioni n.
        """
        return self.n


    def get_epsilon(self):
        """
        Restituisce il valore di epsilon.

        :return: Il valore di epsilon.
        """
        return self.epsilon

    def genera_colorazione_iniziale(self):
        """
        Genera una colorazione valida iniziale casuale per il grafo.

        :param grafo: Un dizionario che rappresenta il grafo.
        :return: Un dizionario che rappresenta la colorazione del grafo.
        """

        # Inizializza la colorazione
        colorazione = {v: 0 for v in self.grafo.keys()}

        # Assegna colori casuali
        for nodo in self.grafo.keys():
            colori_utilizzati = {colorazione[adiacente] for adiacente in self.grafo[nodo] if colorazione[adiacente] != 0}
            colorazione[nodo] = next(c for c in range(1, self.q + 1) if c not in colori_utilizzati)

        return colorazione


    def genera_colorazione_gibbs(self):
        """
        Esegue una q-colorazione del grafo.

        :param grafo: Un dizionario che rappresenta il grafo, dove le chiavi sono i nodi e i valori sono liste di nodi adiacenti.
        :param k: Il numero di colori disponibili.
        :return: Un dizionario che rappresenta la colorazione del grafo.
        """
        # Calcola una q-colorazione f ∈ S qualsiasi


        # pi = lambda f: (lambda grafo, U: filter(lambda , U))
        pi = lambda U: random.choice(
                [colorazione for colorazione in U if all(colorazione[nodo] != colorazione[adiacente] for nodo in self.grafo for adiacente in self.grafo[nodo] if adiacente in colorazione)]
        ) # Funzione di probabilità per la scelta del colore c per il nodo v

        campionatore = CampionatoreDiGibbs(list(self.grafo.keys()), range(1, self.q+1), pi)

        f = self.genera_colorazione_iniziale()
        for _ in range(1, self.n + 1):
            f = campionatore.genera_nuovo_stato(f)

        return f

    def genera_colorazione(self):
        """
        Esegue una q-colorazione del grafo.

        :param grafo: Un dizionario che rappresenta il grafo, dove le chiavi sono i nodi e i valori sono liste di nodi adiacenti.
        :param k: Il numero di colori disponibili.
        :return: Un dizionario che rappresenta la colorazione del grafo.
        """
        # Calcola una q-colorazione f ∈ S qualsiasi

        f = self.genera_colorazione_iniziale()
        # f = {v: random.randint(1, q) for v in grafo.keys()}  # Colorazione casuale iniziale

        for i in range(1, self.n + 1):
            # Calcola j e v
            j = ((i - 1) % self.k)  # Assicurati che j non superi il numero di nodi
            v = list(self.grafo.keys())[j]  # Assicurati che j non superi il numero di nodi

            # Calcola U
            U = {c for c in range(1, self.q + 1) if all(f[w] != c for w in self.grafo[v])}

            #if U:  # Se U non è vuoto
            # Scegli a caso c ∈ U secondo la distribuzione uniforme
            c = random.choice(list(U))
            f[v] = c  # Aggiorna il colore di v

        return f

