# coding: utf8

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: carto.py
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

# Attention: à l'heure de l'écriture de cette version 2, il faut prendre des
# précautions pour installer la bonne version de basemap et de sa dépendance 
# proj4…
# Voir https://github.com/conda-forge/basemap-feedstock/issues/45
# /!\ La ligne conda config effectue un réglage global de conda
#
# Mise en place d'un environnment virtuel:
#       conda config --set channel_priority strict
#       conda create -n livrepython37 python=3.7
#       conda activate livrepython37
# Installation des librairies nécessaires, dans cet environnement:
#       conda install numpy matplotlib basemap proj4=5 pandas
#                                              ^^^^^^^
# Lancement du script, dans cet environnement:
#       python carto.py

# ===== Partie lecture et filtrage des données des villes =============

# Dans la version initiale du livre nous utilisions le module csv et des
# traitements manuels des lignes lues afin de préparer les données.
# Dans la version 2 du livre, cette section est réécrite afin de tirer 
# partie des possibilités offertes par la librairie Pandas.
# Dans le fichier qui liste les villes, les colonnes qui nous intéressent sont:
#    1 Référence département (dont les 2A et 2B de la corse et les 9xx outremer)
#    5 Nom de la commune (nom)
#   16 Population (nbhab)
#   18 Surface km² (surf)
#   19 Longitude (lng)
#   20 Latitude (lat)

# _BEG carto-villes.py
import numpy as np
import pandas as pd

# Lecture à partir du fichier CSV des colonnes qui nous intéressent.
# Source des données: https://sql.sh/736-base-donnees-villes-francaises
villes = pd.read_csv(
        'villes_france.csv', 
        usecols=[1, 5, 16, 18, 19, 20],
        header=None,
        names=['dep', 'nom', 'nbhab', 'surf', 'lng', 'lat'],
        dtype={'dep': np.str} 
        )   

# Suppression des villes non métropolitaines ou à population manquante.
depok = set((f"{x:02d}" for x in range(1, 95+1))) | set(['2A', '2B'])
asupprimer = villes.query("(dep not in @depok) or (nbhab == 0)")
villes.drop(asupprimer.index, axis=0, inplace=True)

# Ajout d'une colonne densité de population résultant d'un calcul.
villes['dens'] = villes['nbhab'] / villes['surf']

print(f"Nombre de villes considérées: {len(villes)}")

villes.to_csv("villes_clean.csv")   # Pour les relire avec un tableur
# _END

# ===== Partie tri et sélection des données à tracer ==================

# _BEG carto-tri.py
# Tri suivant la densité croissante, en modifiant l'ordre des lignes.
villes.sort_values('dens', inplace=True)
# Choix des 200 villes à plus faible densité de population 
selection = villes.iloc[:200]  # Se retrouvent au début grace au tri.

# Le début des données sélectionnées.
print(selection.head(5))
# _END

# ===== Partie sélection des communes et tracé de la carte ============
# Ces deux lignes évitent des messages d'alerte concernant des fonctions de
# matplotlib en cours de dépréciation et encore utilisées par mpl_toolkit
# (à la date d'écriture du script) - vous pouvez les commenter pour voir ces messages
import warnings
warnings.filterwarnings("ignore")

# _BEG carto-carte.py
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

# Choix de la projection, du centrage et de la mise à l'échelle
carte = Basemap(projection='stere', lat_0=46.60611, lon_0=1.87528, 
    resolution='l', llcrnrlon=-5, urcrnrlon=11, llcrnrlat=41, urcrnrlat=51)
# Tracé des lignes de cotes, pays. Couleur pour les continents/la mer.
carte.drawcoastlines(linewidth=0.25)
carte.drawcountries(linewidth=0.25)
carte.fillcontinents(color='#CAAF68', lake_color='#D3FFFF')
carte.drawmapboundary(fill_color='#D3FFFF')
# Lignes parallèles/méridiens tous les 2 degrés
carte.drawmeridians(np.arange(0, 360, 2), linewidth=0.1)
carte.drawparallels(np.arange(-90, 90, 2), linewidth=0.1)
plt.title('Communes à faible densité de population')
# _END

# _BEG carto-points.py
# Utilisation des données sélectionnées, passage de coordonnées lat/long 
# en coordonnées de points sur le graphique.
coords = [carte(lng, lat) for lng, lat in zip(selection.lng, selection.lat)]

# Tracé des points sur la carte
for x, y in coords:
    carte.plot(x, y, marker='o', color='Red', markersize=3)

# Si on veut sauvegarder la figure
plt.savefig("figure.png", dpi=300)  # sinon on commente la ligne
plt.show()                          # affichage de la carte de la France dans une fenêtre
# _END
