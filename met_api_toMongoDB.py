import requests
import time
import json
from pymongo import MongoClient

#Verbindung zur Datenbank, Beispielnamen ggf. ersetzen
client = MongoClient('localhost', 27017)
db = client.APIData
collection = db.botanicals

#Request: Suchanfrage; gibt Anzahl der Ergebnisse und ObjektIDs als .json zurück
anfrage = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/search?q=flowers&isHighlight=true").json()

#Speichert in ids die rückgegebene ID-Liste ein (Vorsicht! Evtl. leeres Ergebnis)
ids = anfrage['objectIDs']

print("Es wurden "+str(anfrage['total'])+" Ergebnisse gefunden.")

#Bearbeitung aller Einzel-IDs in Objekte
for id in ids:
    #Request: Einzelobjekte der Suchanfrage, gibt Einzelobjekte als .json zurück
    objekt = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects/"+str(id)).json()

    #Dokument in Datenbank speichern
    collection.insert_one(objekt)

    #Wenn ein primaryImage vorhanden ist, wird auch dieses abgespeichert
    if objekt["primaryImage"] != "":
        url = objekt['primaryImage']
        #Request: Bilddaten
        data = requests.get(url).content
        #JPG in Datei abspeichern
        with open (str(id)+"_IMG.jpg", "wb") as file:
            file.write(data)
    #sleep-Funktion, um Anzahl der Anfragen pro Sekunde einzuschränken
    time.sleep(0.1)
