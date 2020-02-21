# coding: utf8

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: notesrequetes.py
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

# _BEG notesrequetes_01.py
# File: notesrequetes.py
import sqlite3
import pprint
conn = sqlite3.connect('notes.db') 
c = conn.cursor()
# _END

print("Élèves de 6E2 et leur identificateur unique")
# _BEG notesrequetes_02.py
classe = "6E2"
c.execute("""SELECT nom,idel FROM eleves WHERE classe=? ORDER BY nom;""", (classe,))
res = c.fetchall()
pprint.pprint(res)
# _END

print("Tous les élèves, par classe")
# _BEG notesrequetes_03.py
c.execute("""SELECT classe,nom FROM eleves ORDER BY classe,nom;""")
res = c.fetchall()
classe_actuelle = ""
for classe, eleve in res:
    if classe != classe_actuelle:
        print(f"{classe:=^20}")
        classe_actuelle = classe
    print(f"- {eleve}")
# _END

# Toutes les notes d'un élève:
print("Toutes les notes de Max (id 9) dans toutes les matières:")
# _BEG notesrequetes_04.py
c.execute("""SELECT note FROM notes WHERE elev=9;""")
res = c.fetchall()
print([row[0] for row in res])  # Une seule donnée par tuple
# _END

# Les notes de cet élève en maths, avec les coefficients correspondant.
print("Notes et coefficients de Max en maths:")
# _BEG notesrequetes_05.py
c.execute("""SELECT note,coef
    FROM notes AS N
    JOIN controles AS C
    WHERE N.elev=9 AND N.cont=C.idcon AND C.matiere='maths';
    """)
# _END
res = c.fetchall()
print(res)

# Calcul de la moyenne pondérée par les coefficients pour Max… en Python:
# _BEG notesrequetes_06.py
somme = 0
somcoef = 0
for note,coef in res:
    somme += note * coef
    somcoef += coef
print(f"Moyenne de Max en maths (Python): {somme/somcoef:0.2f}")
# _END

# Calcul de la moyenne pondérée par les coefficients pour Max… en SQL:
# _BEG notesrequetes_07.py
c.execute("""SELECT SUM(note*coef)/SUM(coef)
    FROM notes AS N,controles AS C
    WHERE N.elev=9 AND N.cont=C.idcon AND C.matiere='maths';
    """)
res = c.fetchone()
print(f"Moyenne de Max en maths (SQL): {res[0]:0.2f}")    # Une seule valeur finale.
# _END

# Moyenne pondérée par matière et par élève, triée par classe et élève
print("Moyenne par matière et par élève, triées par classe+élève")
# _BEG notesrequetes_08.py
c.execute("""SELECT classe,nom,matiere,SUM(note*coef)/SUM(coef)
    FROM eleves AS E,controles AS C,notes AS N 
    WHERE E.idel=N.elev AND C.idcon=N.cont 
    GROUP BY E.idel,matiere
    ORDER BY classe,nom,matiere;
    """)
# _END
res = c.fetchall()
pprint.pprint(res)

# Cette requête étant souvent utilisée, on en faire une
# vue moyennes afin de faciliter l'écriture de nouvelles requêtes.
# Elle se comporte comme une table, mais les données sont générées
# dynamiquement, à partir de la requête sous-jacente.
# On supprime préalablement en cas d'exécutions multiples du script
# (tests, modifications…) — la vue elle-même est persistente dans la
# base de données.
c.execute("DROP VIEW IF EXISTS moyennes;")
# _BEG notesrequetes_09.py
c.execute("""CREATE VIEW moyennes AS 
        SELECT classe,nom,matiere,SUM(note*coef)/SUM(coef) AS moy
        FROM eleves AS E,controles AS C,notes AS N 
        WHERE E.idel=N.elev AND C.idcon=N.cont 
        GROUP BY E.idel,matiere;
        """)
# _END

# Meilleur élève par classe et par matière, on utilise la requête
# précédente qui produit une table temporaire dans laquelle on nomme
# la colonne calculée, et on crée notre requête à partir de cette
# nouvelle table temporaire.
print("Meilleur élève par classe et par matière:")
# _BEG notesrequetes_10.py
c.execute("""SELECT classe,nom,matiere,MAX(moy) FROM moyennes
        GROUP BY classe,matiere
        ORDER BY classe,nom,matiere;
        """)
# _END
res = c.fetchall()
pprint.pprint(res)

print("Sans la vue…:")
# _BEG notesrequetes_11.py
c.execute("""SELECT classe,nom,matiere,MAX(moy) FROM
        (SELECT classe,nom,matiere,SUM(note*coef)/SUM(coef) AS moy
            FROM eleves AS E,controles AS C,notes AS N 
            WHERE E.idel=N.elev AND C.idcon=N.cont 
            GROUP BY E.idel,matiere)
        GROUP BY classe,matiere
        ORDER BY classe,nom,matiere;
        """)
# _END
res = c.fetchall()
pprint.pprint(res)

print("Meilleur élève par matière, toutes classes confondues:")
# _BEG notesrequetes_12.py
c.execute("""SELECT classe,nom,matiere,MAX(moy) FROM moyennes
        GROUP BY matiere
        ORDER BY nom,matiere;
        """)
# _END
res = c.fetchall()
pprint.pprint(res)        

# Trouver les homonymes - requête avec une jointure sur la même table.
print("Recherche des homonymes:")
# _BEG notesrequetes_13.py
c.execute("""SELECT A.idel,A.nom 
        FROM eleves AS A, eleves AS B
        WHERE A.idel <> B.idel AND A.nom = B.nom
        ORDER BY A.nom;
        """)
# _END
res = c.fetchall()
pprint.pprint(res)  

# Un contrôle a été trop difficile, correction sur les notes.
print("Correction +1 point dans les notes du contrôle de maths identifié n°8.")
# _BEG notesrequetes_14.py
c.execute("""UPDATE notes SET note=note+1 WHERE cont=8;""")
conn.commit()  # On s'assure que ça persistera.
# _END

# Le contrôle de langue n°29 a été annulé.
print("Suppression des notes du contrôle de langue identifié n°29.")
# _BEG notesrequetes_15.py
numcontrole = 29
c.execute("""DELETE FROM notes WHERE cont=?;""", (numcontrole,))
conn.commit()  # On s'assure que ça persistera.
# _END

conn.close()
