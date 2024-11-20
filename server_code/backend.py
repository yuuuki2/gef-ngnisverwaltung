import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3



@anvil.server.callable
def get_gefaengnisse():
    with sqlite3.connect(data_files['gefaengnis.db']) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gefaengnis")
        gefaengnisse = cursor.fetchall()
    return gefaengnisse

@anvil.server.callable
def get_direktor_und_freie_zellen(gefaengnis_gid):

    verwaltung = app_tables.verwaltung.get(GID=gefaengnis_gid)
    
    if verwaltung:
        return verwaltung['Direktor'], verwaltung['Anzahl_an_freien_Zellen']
    return "Unbekannt", 0  



# Funktion zum Abrufen der Zellen eines bestimmten Gefängnisses
@anvil.server.callable
def get_zellen_aus_gefaengnis(gefaengnis_name):
 
    gefaengnis = app_tables.gefaengnisse.get(Name=gefaengnis_name)
    if gefaengnis:

        zellen = app_tables.zellen.search(GID=gefaengnis['GID'])
        return [(zelle['ZID'], zelle['GID']) for zelle in zellen]
    return [] 



@anvil.server.callable
def get_haeftlinge_aus_zelle(zell_id):
    # Zelle suchen
    zelle = app_tables.zellen.get(ZID=zell_id)
    if zelle:
        # Häftlinge aus der Tabelle 'kann_bewohnen' abrufen
        kann_bewohnen = app_tables.kann_bewohnen.search(ZID=zelle['ZID'])
        haeftlinge = [
            (haeftling['Name'], haeftling['HID']) 
            for kb in kann_bewohnen 
            for haeftling in app_tables.haeftlinge.search(HID=kb['HID'])
        ]
        return haeftlinge
    return [] 
    
 
