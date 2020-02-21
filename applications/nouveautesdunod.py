#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""Présentation des nouveautés Dunod dans une page Web.
"""

# ===== Partie récupération des données ===============================
# _BEG nouveautesdunod_01.py
import urllib.request
import datetime
from collections import namedtuple
import feedparser   # Librairie tierce: installation via pip

# Un tuple pour manipuler une publication avec des attributs nommés.
Publication = namedtuple("Publication", "titre url date")

# Vous pouvez utiliser cette URL dans votre navigateur pour voir le contenu du 
# document téléchargé.
SOURCE_RSS = "https://www.bibliovox.com/feeds/newbooks?publisherid=7"
# _END


# _BEG nouveautesdunod_03.py
def liste_publications(source):
    """Retourne la liste des Publication(tire, url, date) de la source."""
    reponse = urllib.request.urlopen(source)    # Accès au document via HTTP
    doc = reponse.read()                        # Lecture du contenu en bytes
    docrss = doc.decode('utf-8')                # Décodage en chaîne
    rss = feedparser.parse(docrss)
    publis = []
    for pub in rss['entries']:
        titre = pub['title']
        url = pub['link']
        datestr = pub['published'][:10]            # AAAA-MM-JJ…
        # Note Python 3.8 fournit une méthode fromisocalendar().
        date = datetime.datetime.strptime(datestr, "%Y-%m-%d")
        publis.append(Publication(titre, url, date))
    return publis
# _END


# ===== Partie serveur web ============================================
# Documentation Jinja: https://jinja.palletsprojects.com/en/2.10.x/
# Installé à partir du PyPI (sous conda: pip install jinja2)
# _BEG nouveautesdunod_02.py
import http.server
from jinja2 import Template
# _END

# Chaine de modèle pour Jinja2.
# _BEG nouveautesdunod_04.py
MODELE = Template("""\
<html lang="fr">
<head>
    <meta charset="utf-8" />
    <title>Dernières publications de {{ editeur|escape }} chez bibliovox</title>
    <style type="text/css">
    body { background-color: Snow; 
        font-family: "Palatino Linotype", "Book Antiqua", Palatino, serif;
        padding: 1em;}
    h1 { font-family: Arial, Helvetica, sans-serif; color: darkblue; }
    li { padding: 0.2em; }
    .pair { background-color: OldLace; }
    .impair { background-color: PaleGoldenRod; }
    </style>
</head>
<body>
    <h1>Dernières publications de {{ editeur|escape }}</h1>
    <ul id="publications">
    {% for pub in publis|sort(attribute='date',reverse=True) %}
        <li class="{{ loop.cycle('impair', 'pair') }}"><a href="{{ pub.url }}">{{ pub.titre }}</a> ({{ pub.date.strftime("%d/%m/%Y") }})</li>
    {%- endfor %}
    </ul>
</body>
</html> 
""")


def construit_document(nom_editeur, lstpub):
    """Fabrique le document HTML à partir du modèle et des données."""
    return MODELE.render(editeur=nom_editeur, 
                         publis=lstpub)
# _END


# _BEG nouveautesdunod_05.py   
class GestionRequete(http.server.BaseHTTPRequestHandler):
    """À chaque nouvelle requête un objet de cette classe est créé par le serveur."""
    
    def do_GET(self):
        """Appelé pour la fonction GET du protocole HTTP pour accéder au contenu.
        
        Le paramètre s contient des informations sur la requête, et permet
        de fournir le résultat de celle-ci.
        """
        if s.path.lower() == '/dunod':
            lstpublis = liste_publications(SOURCE_RSS)
            dochtml = construit_document("Dunod", lstpublis)
            # Code de retour signalant que c'est ok.
            s.send_response(200)
            # Indication du contenu retourné
            s.send_header("Content-type", "text/html; charset=utf-8") 
            s.end_headers()
            # Contenu à partir d'ici, dans le bon encodage.
            s.wfile.write(dochtml.encode('utf-8'))
        else:
            s.send_response(404)    # Erreur connue: "Not Found"
            s.send_header("Content-type", "text/html; charset=utf-8") 
            s.end_headers()
            s.wfile.write("""\
                <html><body>
                <p>Erreur 404 (essayer <a href="/dunod">/dunod</a>)</p>
                </body></html>""".encode('utf-8'))
# _END


# ===== Programma principal enchaînant les deux parties ===============
# _BEG nouveautesdunod_06.py 
if __name__ == '__main__':
    srv = http.server.HTTPServer(("127.0.0.1", 8080), GestionRequete)
    print("======== Essayer avec votre butineur http://localhost:8080/dunod ========")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    srv.server_close()
# _END
