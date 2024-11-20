from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

class Form1(Form1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
        # Dropdown mit Gefängnissen füllen
        gefaengnisse = anvil.server.call('get_gefaengnisse')
        self.gefaengnisse_drop_down.items = [(gefaengnis[1], gefaengnis[2]) for gefaengnis in gefaengnisse]
        
    
        
    
        self.repeating_zellen.items = [{'zellennummer': 'TODO', 'anzahl_häftlinge': 'TODO'}, 
                                       {'zellennummer': 'TODO', 'anzahl_häftlinge': 'TODO'}]

    def gefaengnisse_drop_down_change(self, **event_args):
        """Dieser Code wird ausgeführt, wenn ein Gefängnis aus dem Dropdown-Menü ausgewählt wird."""
        # Gefängnis ID und Name aus dem Dropdown-Menü
        selected_gefaengnis = self.gefaengnisse_drop_down.selected_value
        gefaengnis_name = selected_gefaengnis[0]  # Name des Gefängnisses
        gefaengnis_gid = selected_gefaengnis[1]  # GID des Gefängnisses

        # Ruft den Direktor und die Anzahl freier Zellen ab
        direktor, freie_zellen = anvil.server.call('get_direktor_und_freie_zellen', gefaengnis_gid)
        
        # Aktualisiert die Labels mit den abgerufenen Daten
        self.label_direktor.text = f"Direktor: {direktor}"
        self.label_freie_zellen.text = f"Freie Zellen: {freie_zellen}"

        # Ruft die Zellen für das ausgewählte Gefängnis ab
        zellen = anvil.server.call('get_zellen_aus_gefaengnis', gefaengnis_name)
        
        # Setzt die Zellen im RepeatingPanel
        self.repeating_zellen.items = [
            {'zellennummer': zelle[0], 'anzahl_häftlinge': self.get_anzahl_haeftlinge(zelle[0])} 
            for zelle in zellen
        ]

    def get_anzahl_haeftlinge(self, zell_id):
        """Berechnet die Anzahl der Häftlinge in einer Zelle."""
        # Ruft die Häftlinge für die Zelle ab
        haeftlinge = anvil.server.call('get_haeftlinge_aus_zelle', zell_id)
        return len(haeftlinge)
