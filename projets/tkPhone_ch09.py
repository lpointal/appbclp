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
        # MODIFICATION ch09        
        self.selection_list = [] # Liste des (nom, numéro tél) sélectionnés
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
        # MODIFICATION ch09        
        # Utilisation de la liste de sélection à la place de la liste
        # issue du fichiers.
        self.selection_list = self.phone_list  # On référence la même liste!
        # Mise à jour de l'affichage de la liste.
        self.cb_rechercher()
        for i in range(0, len(self.selection_list), 2):
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
        # MODIFICATION ch09        
        # Utilisation de la liste de sélection à la place de la liste
        # issue du fichiers.
        self.selection_list = self.phone_list   # On référence la même liste!
        # Mise à jour de l'affichage de la liste.
        self.cb_rechercher()  
        self.ajouter_fichier(nom, tel)
        self.efface_champs()

    def cb_supprimer(self):
        if messagebox.askyesno('Suppression', 'Êtes-vous sûr ?'):
            # maj de la liste
            # MODIFICATION ch09        
            # Important: ici la liste affichée correspond à la liste
            # de sélection, on retrouve donc les éléments dans cette
            # liste.
            nom, tel = self.selection_list[self.index_selection()]
            # On a récupéré nom, tel dans la liste de sélection,
            # on les supprime dans la liste téléphonique aussi.
            self.selection_list.remove(LigneRep(nom, tel))
            self.phone_list.remove(LigneRep(nom, tel))
            # Mise à jour de l'affichage de la liste.
            self.cb_rechercher()  
            self.enregistrer_fichier()
            self.efface_champs()

    def cb_afficher(self, event=None):
        nom, tel = self.selection_list[self.index_selection()]
        self.change_champs(nom, tel)

    # MODIFICATION ch09
    # Définition de la méthode de recherche.
    def cb_rechercher(self, event=None):
        """Recherche à partir d'un filtre."""
        rech = self.valeur_recherche().lower()
        if not rech:
            # Pas de recherche, affichage complet.
            self.selection_list = self.phone_list   # On référence la même liste!
        else:
            # Construction de la liste des références avec des noms 
            # qui contiennent la chaine recherchée (on passe tout en 
            # minuscules pour les comparaisons).
            self.selection_list = [ x for x in self.phone_list  if rech in x.nom.lower() ]
        # Le fait que la méthode issue de la classe parente prenne
        # en paramètre la liste à afficher nous permet de l'utiliser
        # simplement en lui fournissant la liste filtrée.
        self.maj_liste_selection([x.nom for x in self.selection_list])
            
            
# programme principal =========================================================
app = Allo()   # instancie l'application
app.boucle_enevementielle()
