#!/usr/bin/python3
import random
import itertools

class CampionatoreDiGibbs:
    def __init__(self, V, R, pi):

        self.V = V
        self.R = R
        self.RV = [{x: y for x, y in zip(self.V, associazione)} for associazione in  list(itertools.product(self.R, repeat=len(self.V))) ]
        self.pi = pi

    def genera_nuovo_stato(self, stato_corrente):
        A = stato_corrente

        v = random.choice(self.V)
        U = [t for t in self.RV if all(t[w] == A[w] for w in A if w != v)]

        B = self.pi(U)

        return B


