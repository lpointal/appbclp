# Errata à destination des lecteurs qui possèdent le premier tirage de la *deuxième édition* (*Python 3*, éditions Dunod)

- page 37 : orthographe, *on peut utiliser la syntaxe*.

- page 50 : dans le tableau *Les opérations sur les objets de type séquentiel*, pour `s.index(i)` et `s.cout(i)`, ces deux méthodes prennent en paramètre une valeur, pas un indice, il faut donc corriger dans le tableau :

| Opérations  | Signification                                        |
|-------------|------------------------------------------------------|
| `s.index(x)`| indice de la 1<sup>re</sup> occurence de `x` dans `s`|
| `s.count(x)`| nombre d'occurences de `x` dans `s`                  |

- Page 123 : dans la méthode `__add__()` à la construction du résultat `res`, l'ordre des paramètres `lng` et `lat` doit être inversé pour correspondre à l'ordre des paramètres de construction :

    `res = Maison(modele, lat, lng, surface)`

    Ceci a un impact sur les résultats affichés en page 124.

- Page 140 : dans la méthode `cb_supprimer()`, le nom de méthode `self.indexSelection()` appelée doit être changé en `self.index_selection()`.

- page 184 : dans le premier paragraphe, il faut corriger «…, *numpy* fournit le type `np.ndarray`.» (et non *nd.array*).

- page 86 : au milieu de la page, il manque le mot "peut" dans la phrase : «De même, on peut ajouter à `a` un vecteur-colonne de dimension (3, 1).».



