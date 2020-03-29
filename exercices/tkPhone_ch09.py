# coding: utf8

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: tkPhone_ch09.py
# authors: Laurent Pointal <laurent.pointal@limsi.fr>
#          Bob Cordeau <pycours@kordeo.eu>
# license: Creative Commons Attribution-ShareAlike 4.0 International Public
#          License (CC BY-SA 4.0)
#  source: https://github.com/lpointal/appbclp
#    desc: Exercice chap 9 d'adaptation du programme tkPhone.
#     url: https://www.dunod.com/sciences-techniques/python-3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# import ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from collections import namedtuple
from os.path import isfile
# On importe la version modifiée chapitre 9, avec le bouton de recherche.
from tkPhone_IHM_ch09 import AlloIHM
from tkinter import messagebox

SEPARATEUR = '\t'
LigneRep = namedtuple("LigneRep", "nom tel")

# définition de classe ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Allo(AlloIHM):
    """Répertoire téléphonique."""

    def __init__(self, fic='phones.txt'):
        super().__init__()      # => constructeur de l'IHM classe parente.
        self.phone_list = []     # Liste des (nom, numéro tél) à gérer.
        self.fic = ""
        self.charger_fichier(fic)

    def charger_fichier(self, nomfic):
        """Chargement de la liste à partir d'un fichier répertoire."""
        self.fic = nomfic       # Mémorise le nom du fichier
        self.phone_list = []     # Repart avec liste vide.
        if isfile(self.fic):
            with open(self.fic, encoding="utf8") as f:
                for line in f:
                    nom, tel, *reste = line[:-1].split(SEPARATEUR)[:2]
                    self.phone_list.append(LigneRep(nom, tel))
        else:
            with open(self.fic, "w", encoding="utf8"):
                pass
        self.phone_list.sort()
        self.maj_liste_selection([x.nom for x in self.phone_list])
        for i in range(0, len(self.phone_list), 2):
            self.liste_selection.itemconfigure(i, background='#f0f0ff')

    def enregistrer_fichier(self):
        """Enregistre l'ensemble de la liste dans le fichier."""
        with open(self.fic, "w", encoding="utf8") as f:
            for i in self.phone_list:
                f.write("%s%s%s\n" % (i.nom, SEPARATEUR, i.tel))

    def ajouter_fichier(self, nom, tel):
        """Ajoute un enregistrement à la fin du fichier."""
        with open(self.fic, "a", encoding="utf8") as f:
            f.write("%s%s%s\n" % (nom, SEPARATEUR, tel))

    def cb_ajouter(self):
        # maj de la liste
        nom, tel = self.valeurs_champs()
        nom = nom.replace(SEPARATEUR, ' ')  # Sécurité
        tel = tel.replace(SEPARATEUR, ' ')  # Sécurité
        if (nom == "") or (tel == ""):
            self.alerte("Erreur", "Il faut saisir nom et n° de téléphone.")
            return
        self.phone_list.append(LigneRep(nom, tel))
        self.phone_list.sort()
        self.maj_liste_selection([x.nom for x in self.phone_list])
        self.ajouter_fichier(nom, tel)
        self.efface_champs()

    def cb_supprimer(self):
        if messagebox.askyesno('Suppression', 'Êtes-vous sûr ?'):
            # maj de la liste
            nom, tel = self.phone_list[self.index_selection()]
            self.phone_list.remove(LigneRep(nom, tel))
            self.maj_liste_selection([x.nom for x in self.phone_list])
            self.enregistrer_fichier()
            self.efface_champs()

    def cb_afficher(self, event=None):
        nom, tel = self.phone_list[self.index_selection()]
        self.change_champs(nom, tel)

    def cb_rechercher(self, event=None):
        """Recherche à partir d'un filtre."""
        rech = self.valeur_recherche().lower()
        if not rech:
            # Pas de recherche, affichage complet.
            self.maj_liste_selection([x.nom for x in self.phone_list])
        else:
            # Construction de la liste des noms qui contiennent la
            # chaine recherchée (on passe tout en minuscules pour les
            # comparaisons).
            nomsfiltres = [ x.nom for x in self.phone_list if rech in x.nom.lower() ]
            # Le fait que la méthode issue de la classe parente prenne
            # en paramètre la liste à afficher nous permet de l'utiliser
            # simplement en lui fournissant la liste filtrée.
            self.maj_liste_selection(nomsfiltres)
            
            
# programme principal =========================================================
app = Allo()   # instancie l'application
app.boucle_enevementielle()
