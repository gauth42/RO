#!/usr/bin/env python
# coding: utf-8

"""Résolution du flowshop de permutation : 
 """

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019'

import job
import grasp
import sys
import os


class Flowshop:
    def __init__(self, nb_jobs=0, nb_machines=0, optimum=0, l_job=None):
        # nombre de jobs pour le problème
        self.nb_jobs = nb_jobs
        # nombre de machine pour le problème
        self.nb_machines = nb_machines
        # liste des jobs pour le problème
        self.l_job = l_job
        # solution optimale du problème
        self.optimum = optimum

    def nombre_jobs(self):
        return self.nb_jobs

    def nombre_machines(self):
        return self.nb_machines

    def liste_jobs(self, num):
        return self.l_job[num]

    def definir_par(self, nom):
        """ crée un problème de flowshop à partir d'un fichier """
        # ouverture du fichier en mode lecture
        fdonnees = open(nom, "r")
        # lecture de la première ligne
        ligne = fdonnees.readline()
        l = ligne.split()  # on récupère les valeurs dans une liste
        self.nb_jobs = int(l[0])
        self.nb_machines = int(l[1])
        self.optimum = int(l[2])

        self.l_job = []
        for i in range(self.nb_jobs):
            ligne = fdonnees.readline()
            l = ligne.split()
            # on transforme les chaînes de caractères en entiers
            l = [int(i) for i in l]
            j = job.Job(i, l)
            self.l_job += [j]
        # fermeture du fichier
        fdonnees.close()

    def afficher(self):
        for job in self.l_job:
            job.afficher()

    def get_info(self, f_name):
        # Description du problème
        description = ("\nFichier : {}\n"
                       "Nombre de machine : {}\n"
                       "Nombre de jobs : {}\n"
                       "Solution optimale : {}\n"
                       "\n".format(f_name, self.nb_machines, self.nb_jobs, self.optimum))
        return description


if __name__ == "__main__":
    # Récupération des arguments
    file_name = sys.argv[1]

    alpha = float(sys.argv[2])
    biais_type = sys.argv[3]
    do_print = bool(int(sys.argv[4]))

    # Construction du Flowshop
    prob = Flowshop()
    prob.definir_par(file_name)

    # Information sur le problème
    info = prob.get_info(file_name)

    # Execution de la méthode GRASP
    grasp = grasp.Grasp(prob, alpha, biais_type)
    grasp.main()

    # Récupération des résultats
    results = grasp.get_results()

    # Sauvegarde du résultat s'il est meilleur que le précédent
    meilleur = grasp.save_best(file_name)

    # Affichage des informations
    if do_print:
        print(info)
        print("----------------------------------------------------\n"
              "----------------------------------------------------\n")
        print(results)
        print(meilleur)
