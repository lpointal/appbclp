# coding: utf8

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: tkPhone.py
# authors: Laurent Pointal <laurent.pointal@limsi.fr>
#          Bob Cordeau <pycours@kordeo.eu>
# license: Creative Commons Attribution-ShareAlike 4.0 International Public
#          License (CC BY-SA 4.0)
#  source: https://github.com/lpointal/appbclp
#    desc: Ce programme sert de support au livre "Apprendre à programmer avec
#          Python 3", édition Dunod, dans lequel les différentes sections sont
#          expliquées
#     url: https://www.dunod.com/sciences-techniques/python-3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# import ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# _BEG tkPhone_01.py
from collections import namedtuple
from os.path import isfile
from tkPhone_IHM import AlloIHM
from tkinter import messagebox
# _END

SEPARATEUR = '\t'
LigneRep = namedtuple("LigneRep", "nom tel")

# définition de classe ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# _BEG tkPhone_02.py
class Allo(AlloIHM):
    """Répertoire téléphonique."""
# _END

# _BEG tkPhone_03.py
    def __init__(self, fic='phones.txt'):
        super().__init__()      # => constructeur de l'IHM classe parente.
        self.phone_list = []     # Liste des (nom, numéro tél) à gérer.
        self.fic = ""
        self.charger_fichier(fic)
# _END

# _BEG tkPhone_04.py
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
# _END

# _BEG tkPhone_05.py
    def cb_ajouter(self):
        # maj de la liste
        nom, tel = self.valeurs_champs()
        nom = nom.replace(SEPARATEUR, ' ')  # Sécurité
        tel = tel.replace(SEPARATEUR, ' ')  # Sécurité
        if (nom == "") or (tel == ""):
            self.alerte("Erreur", "Il faut saisir nom et n° de téléphone.")
            return
        self.phone_list.append(ligne_rep(nom, tel))
        self.phone_list.sort()
        self.maj_liste_selection([x.nom for x in self.phone_list])
        self.ajouter_fichier(nom, tel)
        self.efface_champs()

    def cb_supprimer(self):
        if messagebox.askyesno('Suppression', 'Êtes-vous sûr ?'):
            # maj de la liste
            nom, tel = self.phone_list[self.indexSelection()]
            self.phone_list.remove(ligne_rep(nom, tel))
            self.maj_liste_selection([x.nom for x in self.phone_list])
            self.enregistrer_fichier()
            self.efface_champs()

    def cb_afficher(self, event=None):
        nom, tel = self.phone_list[self.index_selection()]
        self.change_champs(nom, tel)
# _END

# programme principal =========================================================
# _BEG tkPhone_06.py
app = Allo()   # instancie l'application
app.boucle_enevementielle()
# _END