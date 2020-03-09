# coding: utf8

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: pythoon.py
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

# _BEG pythoon_01.py
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
# _END

# _BEG skimage_8-12.py
def figure(num_fig, image, titre):
    """Préparation de la figure dans la planche."""
    ax[num_fig].imshow(image, cmap=plt.cm.gray)
    ax[num_fig].axis('off')
    ax[num_fig].set_title(titre)
# _END

# Ouverture d'une image format .png dans le répertoire data
# _BEG pythoon_02.py
pythoon = io.imread("pythoon.png")
# _END

# Une planche de 3 figures
# _BEG pythoon_03.py
_, ax = plt.subplots(1, 3)

# Pythoon
figure(0, pythoon, 'Pythoon')
# _END

# _BEG pythoon_04.py
# Dimensions de l'image
nl, nc, _ = pythoon.shape
print(f"lignes : {nl}; colonnes : {nc}")
# Grille de la dimension de l'image
X, Y = np.ogrid[0:nl, 0:nc]
# Création d'un masque ciculaire
masque = (X-nl / 2)**2 + (Y-nc / 2)**2 > nl*nc / 8

# Le masque
figure(1, masque, 'Masque')

# Application du masque sur l'image
pythoon[masque] = 150

# Le pythoon dans le masque
figure(2, pythoon, 'Pythoon dans le masque')

# Tracer de la planche n°1
plt.show()
# _END

# 2nd planche de 3 figures
# _BEG pythoon_05.py
_, ax = plt.subplots(1, 3)

# Symétrie haut-bas
pythoon_ud = np.flipud(pythoon)
figure(0, pythoon_ud, "Up-down")

# Symétrie gauche-droite
pythoon_lr = np.fliplr(pythoon)
figure(1, pythoon_lr, "Gauche-droite")

# # Rotation de 90°
pythoon_rot90 = np.rot90(pythoon)
figure(2, pythoon_rot90, "À gauche")

# Tracer de la planche n°2
plt.show()
# _END
