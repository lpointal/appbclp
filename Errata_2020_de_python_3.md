# Errata à destination des lecteurs qui possèdent le pemier tirage de la *seconde édition*<br>(*Python 3*, éditions Dunod)

- Page 140 : dans la méthode `cb_supprimer`, le nom de méthode `self.indexSelection()` appelée doit être changé en `self.index_selection()`.
- Page 123 : dans la méthode `__add__` à la construction du résultat `res`, l'ordre des paramètres `lng` et `lat` doit être inversé pour correspondre à l'ordre des paramètres de construction :

        res = Maison(modele, lat, lng, surface)
    
  Ceci a un impact sur les résultat affichés en page 124.
