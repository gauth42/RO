#!/usr/bin/env python
# coding: utf-8

""" Classe GRASP """

import ordonnancement
import numpy as np
from bisect import bisect
import time


class Grasp():
    def __init__(self, flowshop):
        """
        Initalisation de la méthode GRASP

        :param flowshop:  flowshop du problème
        """
        # Problème de Flowshop
        self.prob = flowshop

        # Creation de l'ordonnancement
        self.ordo = ordonnancement.Ordonnancement(self.prob.nb_machines)

        # Paramètre alpha de la méthode
        self.alpha = 0.5

        # Choix du biais
        self.bias = "linéaire"

        # Jobs restant à placer dans l'ordonnancement
        self.jobs = []
        self.maj_jobs()

        # Temps d'exécution
        self.temps_exe = 0

    def main(self):
        """
        Application de la méthode
        """
        start = time.time()
        for i in range(self.prob.nb_jobs-1):

            temps_completion = {}
            for job in self.jobs:
                temps_completion[job.numero()] = self.ordo.hypothetic_ordonnancer_job(job)

            # Calcul du RCL
            min_time, max_time = np.min(list(temps_completion.values())), np.max(list(temps_completion.values()))
            RCL = [min_time, min_time + (max_time - min_time) * self.alpha]

            # Choix des jobs dans le RCL
            jobs_eligible = [job for job in self.jobs if temps_completion[job.numero()] <= RCL[1]]
            rang_dict = dict(zip([job.numero() for job in jobs_eligible],
                                 np.argsort([temps_completion[job.numero()] for job in jobs_eligible]) + 1))

            # Calcul des probabilités des jobs dans le RCL
            fitness, proba_dict = linear_bias(rang_dict)

            # Choix du job à placer dans la séquence d'ordonnancemenr
            u = np.random.rand()
            proba = np.array(list(proba_dict.values()))
            for j in range(1, len(proba)):
                proba[j] += proba[j-1]
            index = bisect(proba, u)

            num_choisi = np.array(list(proba_dict.keys()))[index]
            job_choisi = [job for job in self.jobs if job.numero() == num_choisi][0]

            self.ordo.ordonnancer_job(job_choisi)
            self.maj_jobs()

            # Décommenter pour afficher l'évolution de l'algorithm à chaque étape
            affichage = ("---------------------------------------------------- \n"
                         "Iteration number : {}\n"
                         "Jobs restant à placer : {}\n"
                         "Valeur de alpha : {}\n"
                         "RCL : {}\n"
                         "Rang des jobs dans RCL : {}\n"
                         "Probabilités des jobs : {}\n"
                         "Valeur de u : {:.3f}\n"
                         "Job choisi : {}\n"
                         "Etat actuel de la séquence : {}\n"
                         "Valeur actuelle du Makespan : {}\n"
                         .format(i, [job.numero() for job in self.jobs], self.alpha, RCL, rang_dict,
                                 dict(zip(proba_dict.keys(), [round(x, 3) for x in proba_dict.values()])), u,
                                 num_choisi, [job.numero() for job in self.ordo.seq], self.ordo.duree()))

            #print(affichage)

        # Ajout du dernier job restant à la séquence
        self.ordo.ordonnancer_job(self.jobs[0])

        # Calcul du temps pris par la méthode
        self.temps_exe = time.time() - start

    def maj_jobs(self):
        """
        Met à jour la liste des jobs restant à placer dans l'ordonnancement
        """
        self.jobs = [job for job in self.prob.l_job if job not in self.ordo.seq]


def linear_bias(rang_dict):
    """

    :param rang_dict: dictionnaire des rangs des jobs dans le RCL
    :return: fitness:
             proba_dict: dictionnaire des probabilités des jobs dans le RCL
    """
    bias = 1/np.array(list(rang_dict.values()))
    fitness = sum(bias)
    proba_dict = dict(zip(rang_dict.keys(), bias/fitness))

    return fitness, proba_dict


if __name__ == "__main__":
    pass