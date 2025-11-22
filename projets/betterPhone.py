# coding: utf8

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: betterPhone.py
# authors: Laurent Pointal <laurent.pointal@limsi.fr>
#          Bob Cordeau <pycours@kordeo.eu>
# license: Creative Commons Attribution-ShareAlike 4.0 International Public
#          License (CC BY-SA 4.0)
#  source: https://github.com/lpointal/appbclp
#    desc: Révision ergonomique et esthétique du programme tkPhone.
#     url: https://www.dunod.com/sciences-techniques/python-3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# import ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from collections import namedtuple
from os.path import isfile
import unicodedata
# On importe la version modifiée chapitre 9, avec le bouton de recherche.
from betterPhone_IHM import AlloIHM
from tkinter import messagebox

SEPARATEUR = '\t'
# Amélioration lors des filtrages / recherche.
# Lorsque lu en mémoire, on ajoute un champs filtre qui contient la valeur
# du nom prête pour des recherches (sans accent, sans espace, en minuscules).
LigneRep = namedtuple("LigneRep", "nom tel filtre")


# Fonctions outils ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def creer_filtre(nom):
    """Retourne la valeur de filtre correspondant au nom.
    
    Concertit les caractères accentués.
    Supprime les espaces et marques.
    """
    # La catégorie unicode est une combinaison de 2 caractères, dont
    # la première peut être L lettre, M marque, N nombre, P ponctuation,
    # S symbole, Z séparateur ou C autre. 
    # Ici on ne conserve que les lettres.
    nom = nom.lower()
    filtre = ''.join((c for c in unicodedata.normalize('NFD', nom) 
                              if unicodedata.category(c).startswith('L')))
    return filtre


# définition de classe ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Allo(AlloIHM):
    """Répertoire téléphonique."""

    def __init__(self, fic='phones.txt'):
        super().__init__()      # => constructeur de l'IHM classe parente.
        self.phone_list = []     # Liste des (nom, numéro tél) à gérer.
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
                    filtre = creer_filtre(nom)
                    self.phone_list.append(LigneRep(nom, tel, filtre))
        else:
            with open(self.fic, "w", encoding="utf8"):
                pass
        self.phone_list.sort()
        self.selection_list = self.phone_list  # Utilise la même liste
        self.efface_champs()
        self.efface_rechercher()
        self.cb_rechercher()    # Provoque la mise à jour graphique.

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
        filtre = creer_filtre(nom)
        self.phone_list.append(LigneRep(nom, tel, filtre))
        self.phone_list.sort()
        # MODIFICATION ch09        
        # Utilisation de la liste de sélection à la place de la liste
        # issue du fichiers.
        self.selection_list = self.phone_list   # On référence la même liste!
        # Mise à jour de l'affichage de la liste.
        self.ajouter_fichier(nom, tel)
        self.efface_champs()
        self.cb_rechercher()  

    def cb_supprimer(self):
        if messagebox.askyesno('Suppression', 'Êtes-vous sûr ?'):
            nom, tel, filtre = self.selection_list[self.index_selection()]
            # On a récupéré nom, tel dans la liste de sélection,
            # on les supprime dans la liste téléphonique aussi.
            self.selection_list.remove(LigneRep(nom, tel, filtre))
            self.phone_list.remove(LigneRep(nom, tel, filtre))
            # Mise à jour de l'affichage de la liste.
            self.enregistrer_fichier()
            self.efface_champs()
            self.cb_rechercher()  # Note: en conservant le filtre recherche

    def cb_afficher(self, event=None):
        nom, tel, filtre = self.selection_list[self.index_selection()]
        self.change_champs(nom, tel)

    def cb_rechercher(self, event=None):
        """Recherche à partir d'un filtre."""
        rech = creer_filtre(self.valeur_recherche().lower())
        # On attend au moins 2 caractères pour rechercher, si
        # il n'y a pas assez on fait un affichage complet.
        if len(rech) < 2:
            self.selection_list = self.phone_list   # On référence la même liste!
        else:
            self.selection_list = [ x for x in self.phone_list 
                                                     if rech in x.filtre ]
        self.maj_liste_selection([x.nom for x in self.selection_list])
            
            
# programme principal =========================================================
app = Allo()   # instancie l'application
app.boucle_enevementielle()
