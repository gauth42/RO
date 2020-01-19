#!/usr/bin/env python
# coding: utf-8

""" Classe GRASP """

import ordonnancement
import numpy as np
from bisect import bisect
import time
import os


class Grasp:
    def __init__(self, flowshop, alpha, biais_type):
        """
        Initalisation de la méthode GRASP

        :param flowshop:  flowshop du problème
        """
        # Problème de Flowshop
        self.prob = flowshop

        # Creation de l'ordonnancement
        self.ordo = ordonnancement.Ordonnancement(self.prob.nb_machines)

        # Paramètre alpha de la méthode
        self.alpha = alpha

        # Choix du biais
        self.biais_type = biais_type

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

            # Jobs restant à placer
            jobs_restant = [job.numero() for job in self.jobs]

            # Plusieurs jobs ont le même Cmax
            if RCL[0] == RCL[1]:
                pass
                jobs_eligible = [job for job in self.jobs if temps_completion[job.numero()] <= RCL[1]]

                job_choisi = jobs_eligible[0]
                num_choisi = job_choisi.numero()

                self.ordo.ordonnancer_job(job_choisi)
                self.maj_jobs()

                affichage = ("---------------------------------------------------- \n"
                             "L'algorithme est greedy et plusieurs jobs ont le même completion time \n"
                             "On choisit toujours le premier de cette liste \n"
                             "Iteration number : {}\n"
                             "Jobs restant à placer : {}\n"
                             "Valeur de alpha : {}\n"
                             "RCL : {}\n"
                             "Job choisi : {}\n"
                             "Etat actuel de la séquence : {}\n"
                             "Valeur actuelle du Makespan : {}\n"
                             .format(i, jobs_restant, self.alpha,
                                     RCL,
                                     num_choisi, [job.numero() for job in self.ordo.seq], self.ordo.duree()))

            else:
                # Choix des jobs dans le RCL
                jobs_eligible = [job for job in self.jobs if temps_completion[job.numero()] <= RCL[1]]
                rang_dict = dict(zip([job.numero() for job in jobs_eligible],
                                     np.argsort([temps_completion[job.numero()] for job in jobs_eligible]) + 1))

                # Calcul des probabilités des jobs dans le RCL
                fitness, proba_dict = bias(self.biais_type, rang_dict)

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
                             .format(i, jobs_restant, self.alpha, RCL, rang_dict,
                                     dict(zip(proba_dict.keys(), [round(x, 3) for x in proba_dict.values()])), u,
                                     num_choisi, [job.numero() for job in self.ordo.seq], self.ordo.duree()))
            # print(affichage)

        # Ajout du dernier job restant à la séquence
        self.ordo.ordonnancer_job(self.jobs[0])

        # Calcul du temps pris par la méthode
        self.temps_exe = time.time() - start

    def maj_jobs(self):
        """
        Met à jour la liste des jobs restant à placer dans l'ordonnancement
        """
        self.jobs = [job for job in self.prob.l_job if job not in self.ordo.seq]

    def get_results(self):
        res = ("Résultats de la méthode \n"
               "Cmax : {}\n"
               "Ecart de l'optimum : {}\n"
               "Ecart relatif de l'optimum : {:.2f} %\n"
               "\n"
               "Greedy paramètre alpha : {}\n"
               "Biais : {}\n"
               "Temps d'excécution : {:.5f} s"
               "".format(self.ordo.duree(), self.ordo.duree() - self.prob.optimum,
                         (self.ordo.duree() - self.prob.optimum) / self.ordo.duree() * 100,
                         self.alpha, self.biais_type, self.temps_exe))
        return res

    def save_best(self, file_name):
        if file_name.find('/') > 0:
            dir_name = file_name[:file_name.find('/')]
        else:
            dir_name = None

        res = self.get_results()

        # Sauvegarde de l'ordonanncement dans les logs si la séquence est meilleure que les précédentes
        log = res + "\n" + "\n" + self.ordo.afficher()
        meilleur = ""

        if not os.path.exists("logs/" + file_name):
            if dir_name is not None and not os.path.exists("logs/" + dir_name):
                os.mkdir("logs/" + dir_name)
            f = open("logs/" + file_name, "x")
            f.write(log)
            f.close()
            print(
                "Ecart de l'optimum : {:.2f} %".format((self.ordo.duree() - self.prob.optimum) /
                                                       self.ordo.duree() * 100))
        else:
            flog = open("logs/" + file_name, "r")
            lignes = flog.readlines()
            actual_best = int(lignes[1].split()[-1])
            flog.close()
            if self.ordo.duree() < actual_best:
                meilleur = "La solution a été amélioré : \n" \
                           "      - ancienne solution : {}\n" \
                           "      - nouvelle solution : {}\n" \
                           "Nouvel écart de l'optimum : {}".format(actual_best, self.ordo.duree(),
                                                                   (self.ordo.duree() - self.prob.optimum)
                                                                   / self.ordo.duree() * 100)
                fnew = open("logs/" + file_name, "w")
                fnew.write(log)
                fnew.close()
        return meilleur

def bias(biais_type, rang_dict):
    """

    :param biais_type: type du biais
    :param rang_dict: dictionnaire des rangs des jobs dans le RCL
    :return: fitness:
             proba_dict: dictionnaire des probabilités des jobs dans le RCL
    """
    if biais_type == "lineaire":
        bias_lin = 1/np.array(list(rang_dict.values()))
        fitness = sum(bias_lin)
        proba_dict = dict(zip(rang_dict.keys(), bias_lin/fitness))

        return fitness, proba_dict


if __name__ == "__main__":
    pass