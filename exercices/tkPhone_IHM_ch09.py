# coding: utf8

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: tkPhone_IHM_ch09.py
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

# Doc tkinter très complète : http://tkinter.fdex.eu/

import tkinter as tk
from tkinter import messagebox

class AlloIHM:
    """IHM de l'application 'répertoire téléphonique'."""
    def __init__(self):
        """Initialisateur/lanceur de la fenêtre de base"""
        self.root = tk.Tk()     # Fenêtre de l'application
        self.root.option_readfile('tkOptions.txt')  # Options de look
        self.root.title("Allo !")
        self.root.config(relief=tk.RAISED, bd=3)
        self.construire_widgets()

    def boucle_enevementielle(self):
        self.champs_nom.focus()
        self.root.mainloop()

    def construire_widgets(self):
        """Configure et positionne les widgets"""
        # frame "valeurs_champs" (en haut avec bouton d'effacement)
        frame_h = tk.Frame(self.root, relief=tk.GROOVE, bd=2)
        frame_h.pack(fill=tk.X)
        frame_h.columnconfigure(1, weight=1)

        tk.Label(frame_h, text="Nom :").grid(row=0, column=0, sticky=tk.E)
        self.champs_nom = tk.Entry(frame_h)
        self.champs_nom.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=10)

        tk.Label(frame_h, text="Tel :").grid(row=1, column=0, sticky=tk.E)
        self.champs_tel = tk.Entry(frame_h)
        self.champs_tel.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=2)

        # MODIFICATION ch09
        # Un frame occupant la 3ème ligne du frame_h permet de positionner
        # le bouton Effacer, et d'ajouter un champs de saisie et un bouton 
        # Rechercher.
        # Ajout attribut: self.champs_rech
        frame_h1 = tk.Frame(frame_h, relief=tk.GROOVE)
        frame_h1.grid(row=2, column=0, columnspan=2, pady=3)
        b = tk.Button(frame_h1, text="Effacer ", command=self.efface_champs)
        b.grid(row=0, column=0, pady=3)
        self.champs_rech = tk.Entry(frame_h1)
        self.champs_rech.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)
        b = tk.Button(frame_h1, text="Rechercher ", command=self.cb_rechercher)
        b.grid(row=0, column=2, pady=3)

        # frame "liste" (au milieu)
        frame_m = tk.Frame(self.root)
        frame_m.pack(fill=tk.BOTH, expand=True)

        self.scroll = tk.Scrollbar(frame_m)
        self.liste_selection = tk.Listbox(frame_m, yscrollcommand=self.scroll.set,
                                        height=20)
        self.scroll.config(command=self.liste_selection.yview)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        self.liste_selection.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)
        self.liste_selection.bind("<Double-Button-1>",
                    lambda event: self.cb_afficher(event))

        # frame "boutons" (en bas)
        frame_b = tk.Frame(self.root, relief=tk.GROOVE, bd=3)
        frame_b.pack(pady=3, side=tk.BOTTOM, fill=tk.NONE)

        b1 = tk.Button(frame_b, text="Ajouter  ", command=self.cb_ajouter)
        b2 = tk.Button(frame_b, text="Supprimer", command=self.cb_supprimer)
        b3 = tk.Button(frame_b, text="Afficher ", command=self.cb_afficher)
        b1.pack(side=tk.LEFT, pady=2)
        b2.pack(side=tk.LEFT, pady=2)
        b3.pack(side=tk.LEFT, pady=2)

    # Méthodes d'échange d'informations application <==> GUI
    def maj_liste_selection(self, lstnoms):
        """Remplissage complet de la liste à sélection avec les noms."""
        self.liste_selection.delete(0, tk.END)
        for nom in lstnoms:
            self.liste_selection.insert(tk.END, nom)

    def index_selection(self):
        """Retourne le n° de la ligne actuellement sélectionnée."""
        return int(self.liste_selection.curselection()[0])

    def change_champs(self, nom, tel):
        """Modification des affichages dans les champs de saisie."""
        self.champs_nom.delete(0, tk.END)
        self.champs_nom.insert(0, nom)
        self.champs_tel.delete(0, tk.END)
        self.champs_tel.insert(0, tel)
        self.champs_nom.focus()

    def efface_champs(self):
        """Effacement des champs de saisie."""
        # MODIFICATION ch09
        # On efface le champs pour la recherche.
        # Et on effectue une remise à jour de la liste afin d'avoir tous
        # les noms affichés.
        self.champs_rech.delete(0, tk.END)
        self.cb_rechercher()
        self.change_champs('', '')
        
    def valeurs_champs(self):
        """Retourne la saisie nom/tél actuelle."""
        nom = self.champs_nom.get()
        tel = self.champs_tel.get()
        return nom, tel

    def alerte(self, titre, message):
        """Affiche un message à l'utilisateur."""
        messagebox.showinfo(titre, message)

    # Méthodes à redéfinir dans l'application (actions liées aux boutons).
    def cb_ajouter(self):
        """Ajout dans la liste du contenu des champs de saisie."""
        raise NotImplementedError("cb_ajouter à redéfinir")

    def cb_supprimer(self):
        """Suppression de la liste de l'entrée des champs de saisie."""
        raise NotImplementedError("cb_supprimer à redéfinir")

    def cb_afficher(self, event=None):
        """Affichage dans les champs de saisie de la sélection."""
        raise NotImplementedError("cb_afficher à redéfinir")

    # MODIFICATION ch09
    # On a ajouté une méthode callback liée au bouton Rechercher.
    def cb_rechercher(self, event=None):
        """Recherche à partir d'un filtre."""
        raise NotImplementedError("cb_rechercher à redéfinir")

    # MODIFICATION ch09
    # On a ajouté une méthode afin de récupérer la valeur de recherche
    # sans avoir à accéder directement au contrôle.
    def valeur_recherche(self):
        """Retourne la saisie recherche actuelle."""
        return self.champs_rech.get()


# auto-test ===================================================================
if __name__ == '__main__':
    # instancie l'IHM, callbacks inactifs
    app = AlloIHM()
    app.boucle_enevementielle()
