# coding: utf8

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: notesinitdb.py
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

# _BEG notesinitdb_01.py
# Fichier: notesinitdb.py
import sqlite3
conn = sqlite3.connect('notes.db')
c = conn.cursor()
# _END

# Suppression des structures et données existantes, de façon à pouvoir ré-exécuter
# le script plusieurs fois en partant d'une base vide.
c.execute("DROP VIEW IF EXISTS moyennes;")
c.execute("DROP TABLE IF EXISTS notes;")
c.execute("DROP TABLE IF EXISTS controles;")
c.execute("DROP TABLE IF EXISTS eleves;")
# Note: les index sont automatiquement supprimés avec les tables.
conn.commit()

# ========== SCHEMA DE LA BASE ============================================
# Mise en place de la structure.
# Le passage par un programme permet de très rapidement remettre en place
# une base avec une structure définie, qui peut tout de suite être utilisée
# pour manipuler des données.
# _BEG notesinitdb_02.py
c.execute("""CREATE TABLE 'eleves' (
    idel INT PRIMARY KEY NOT NULL,
    nom VARCHAR(100) NOT NULL,
    classe VARCHAR(10) NOT NULL
    );""")
c.execute("""CREATE TABLE 'controles' (
    idcon INT PRIMARY KEY NOT NULL,
    matiere VARCHAR(20) NOT NULL,
    coef FLOAT NOT NULL
    );""")
c.execute("""CREATE TABLE 'notes' (
    elev INT NOT NULL,
    cont INT NOT NULL,
    note FLOAT,
    FOREIGN KEY(elev) REFERENCES eleves(idel),
    FOREIGN KEY(cont) REFERENCES controles(idcon)
    );""")
# _END
# _BEG notesinitdb_03.py
c.execute("""CREATE UNIQUE INDEX idxeleves ON eleves(idel);""")
c.execute("""CREATE UNIQUE INDEX idxcontroles ON controles(idcon);""")
c.execute("""CREATE INDEX idxnotes1 ON notes(elev);""")
c.execute("""CREATE INDEX idxnotes2 ON notes(cont);""")
c.execute("""CREATE UNIQUE INDEX idxnotes3 ON notes(elev,cont);""")
# _END
# Là on valide les requêtes, le schéma de la base de données est défini.
conn.commit()

# ========== DONNEES ======================================================
# Insertion des données d'élèves et de contrôles.
# Plutôt que de reprendre la description des données en SQL,
# on utilise l'import à partir d'un fichier texte CSV (colonnes
# séparées par des virgules).
# Note: l'interface ligne de commande de sqlite3 contient une commande
# .import qui réalise automatiquement l'import de données CSV.
# Note: Les données dans les fichiers CSV sont dans le même ordre que les colonnes
# dans les tables correspondantes.
# _BEG notesinitdb_04.py
import csv
with open("eleves.csv", encoding="utf8") as f:
    lecteurcsv = csv.reader(f)
    c.executemany("""INSERT INTO eleves(idel, nom, classe) VALUES (?, ?, ?);""", lecteurcsv)

with open("controles.csv", encoding="utf8") as f:
    lecteurcsv = csv.reader(f)
    c.executemany("""INSERT INTO controles(idcon, matiere, coef) VALUES (?, ?, ?);""", lecteurcsv)
conn.commit()
# _END

# Note: en utilisant: pandas et son interface vers les bases de données:
#import pandas as pd
#df = pd.read_csv(open("eleves.csv", encoding="utf8"))
#df.to_sql("eleves", conn, if_exists='append', index=False)

# Pour les notes, on pourrait disposer de données au format CSV et les importer
# de la même façon, mais pour l'exemple on va générer des données de notes
# aléatoires.
# On récupère un produit cartésien qui donne toutes les combinaisons entre
# les ids d'élèves et les ids de contrôles. Trié pour avoir toujours le même
# ordre à chaque exécution.
# _BEG notesinitdb_05.py
c.execute("""SELECT idel,idcon
    FROM eleves
    JOIN controles
    ORDER BY idel,idcon;
    """)
lstids = c.fetchall()   # Données récupérées, le curseur est à nouveau utilisable
# _END

# _BEG notesinitdb_06.py
import random
random.seed(1)  # Pour avoir toujours les mêmes séries, donc les mêmes résultats.
for ide,idc in lstids:
    if random.randint(1,100) <= 5:  # Dans ~5% des cas, pas de note (absences…)
        continue
    note = random.randint(50,180) / 10  # Note avec 1 décimale.
    c.execute("INSERT INTO notes(elev,cont,note) VALUES (?, ?, ?)", (ide, idc, note))
conn.commit()
# _END

# Récupération des identificateurs d'élèves
# L'exécution récupère une liste de tuples contenant les n-uplets sélectionnés par
# la requête.
#c.execute("SELECT idel FROM eleves;")
#ideleves = [row[0] for row in c.fetchall()]

## Récupératio des identificateurs de contrôles
#c.execute("SELECT idcon FROM controles;")
#idcontroles = [row[0] for row in c.fetchall()]

## Création d'une note par élève par contrôle, sauf dans ~5% des cas (absences…)
#import random
#random.seed(1)  # Pour avoir toujours les mêmes séries, donc les mêmes résultats.
#for ide in ideleves:
    #for idc in idcontroles:
        #if random.randint(1,100) <= 5:  # Les cas à passer.
            #continue
        #note = random.randint(50,180) / 10  # Note avec 1 décimale.
        #c.execute("INSERT INTO notes(elev,cont,note) VALUES (?, ?, ?)", (ide, idc, note))
#conn.commit()

conn.close()
