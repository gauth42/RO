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


class Flowshop():
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


if __name__ == "__main__":
    # Récupération des arguments
    file_name = sys.argv[1]
    if file_name.find('/') > 0:
        dir_name = file_name[:file_name.find('/')]
    else:
        dir_name = None

    do_print = bool(int(sys.argv[2]))

    # Construction du Flowshop
    prob = Flowshop()
    prob.definir_par(file_name)

    # Ajout de tous les jobs au flowshop
    for i in range(prob.nb_jobs):
        j = prob.liste_jobs(i)

    # Information sur le problème
    info = ("\nFichier : {}\n" \
            "Nombre de machine : {}\n"
            "Nombre de jobs : {}\n"
            "Solution optimale : {}\n"
            "\n".format(file_name, prob.nb_machines, prob.nb_jobs, prob.optimum))

    # Execution de la méthode GRASP
    grasp = grasp.Grasp(prob)
    grasp.main()

    res = ("Résultats de la méthode \n"
           "Cmax : {}\n"
           "Ecart de l'optimum : {}\n"
           "Ecart relatif de l'optimum : {:.2f} %\n"
           "Greedy paramètre alpha : {}\n"
           "Biais : {}\n"
           "Temps d'excécution : {:.5f} s"
           "".format(grasp.ordo.duree(), grasp.ordo.duree() - prob.optimum,
                     (grasp.ordo.duree() - prob.optimum) / grasp.ordo.duree() * 100,
                     grasp.alpha, grasp.bias, grasp.temps_exe))

    # Sauvegarde de l'ordonanncement dans les logs si la séquence est meilleure que les précédentes
    log = res + "\n" + grasp.ordo.afficher()
    meilleur = ""

    if not os.path.exists("logs/" + file_name):
        if dir_name is not None and not os.path.exists("logs/" + dir_name):
            os.mkdir("logs/" + dir_name)
        f = open("logs/" + file_name, "x")
        f.write(log)
        f.close()
        print("Ecart de l'optimum : {:.2f} %".format((grasp.ordo.duree() - prob.optimum) / grasp.ordo.duree() * 100))
    else:
        flog = open("logs/" + file_name, "r")
        lignes = flog.readlines()
        actual_best = int(lignes[1].split()[-1])
        flog.close()
        if grasp.ordo.duree() < actual_best:
            meilleur = "La solution a été amélioré : \n" \
                  "      - ancienne solution : {}\n" \
                  "      - nouvelle solution : {}".format(actual_best, grasp.ordo.duree())
            fnew = open("logs/" + file_name, "w")
            fnew.write(log)
            fnew.close()
            if not do_print:
                print("Ecart de l'optimum : {:.2f} %".format((grasp.ordo.duree() - prob.optimum) / grasp.ordo.duree() * 100))

    # Affichage des informations
    if do_print:
        print(info)
        print("----------------------------------------------------\n"
              "----------------------------------------------------\n")
        print(res)
        print(meilleur)