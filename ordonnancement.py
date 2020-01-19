#!/usr/bin/env python
# coding: utf-8

""" Classe Ordonnancement """

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019'

import job


class Ordonnancement:
    # constructeur pour un ordonnancement vide
    def __init__(self, nb_machines):
        # séquence des jobs
        self.seq = []
        # nombre de machines
        self.nb_machines = nb_machines
        # durée totale de l'ordonnancement
        self.dur = 0
        # date à partir de laquelle chaque machine est libre
        self.date_dispo = [0 for i in range(self.nb_machines)]

    def duree(self):
        return self.dur
    
    def sequence(self):
        return self.seq
    
    def date_disponibilite(self, num_machine):
        return self.date_dispo[num_machine]

    def date_debut_operation(self, job, operation):
        return job.date_deb[operation]

    def fixer_date_debut_operation(self, job, operation, date):
        job.date_deb[operation] = date

    def afficher(self):
        res = "Ordre des jobs : "
        for job in self.seq:
            res += "{} ".format(job.numero())
        res += "\n"
        for job in self.seq:
            res += "Job {} : ".format(job.numero())
            for mach in range(self.nb_machines):
                res += "op {} à t = {} | ".format(mach, self.date_debut_operation(job, mach))
            res += "\n"
        res += "Cmax = {}".format(self.dur)
        return res

    # ajoute un job dans l'ordonnancement
    # à la suite de ceux déjà ordonnancés
    def ordonnancer_job(self, job):
        self.seq += [job]
        for mach in range(self.nb_machines):
            if mach == 0:   # première machine
                self.fixer_date_debut_operation(job, 0, self.date_dispo[0])
            else:   # machines suivantes
                date = max(self.date_dispo[mach-1], self.date_dispo[mach])
                self.fixer_date_debut_operation(job, mach, date)
            self.date_dispo[mach] = self.date_debut_operation(job, mach) + \
            job.duree_operation(mach)
        self.dur = max(self.dur, self.date_dispo[self.nb_machines-1])

    # ajoute les jobs d'une liste dans l'ordonnancement
    # à la suite de ceux déjà ordonnancés
    def ordonnancer_liste_job(self, liste_jobs):
        for job in liste_jobs:
            self.ordonnancer_job(job)

    # Calcul la nouvelle durée hypotéhtique en ajoutant un nouveau job
    # sans modifier les variables de l'object
    def hypothetic_ordonnancer_job(self, job):
        seq = self.seq +[job]
        date_dispo = self.date_dispo.copy()
        date_deb = job.date_deb

        for mach in range(self.nb_machines):
            if mach == 0:  # première machine
                date_deb[mach] = date_dispo[0]
            else:  # machines suivantes
                date = max(date_dispo[mach - 1], date_dispo[mach])
                date_deb[mach] = date
            date_dispo[mach] = date_deb[mach] + job.duree_operation(mach)
        return max(self.dur, date_dispo[self.nb_machines - 1])

# "main" pour tester la classe   
if __name__ == "__main__":
    a = job.Job(1,[1,1,1,1,10])
    b = job.Job(2,[1,1,1,4,8])
    a.afficher()
    b.afficher()
    l = [a,b]
    ordo = Ordonnancement(5)
    ordo.ordonnancer_job(a)
    ordo.ordonnancer_job(b)
    ordo.sequence()
    print(ordo.afficher())
    a.afficher()
    b.afficher()
