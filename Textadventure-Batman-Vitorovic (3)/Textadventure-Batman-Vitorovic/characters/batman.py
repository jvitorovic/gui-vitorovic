"""
Modul für die Definition des Batman-Charakters.

Klassen:
    Batman: Abgeleitete Klasse, die Batman als spielbaren Charakter repräsentiert.
"""

from characters.character import Character

class Batman(Character):
    """
    Repräsentiert Batman als spielbaren Charakter.

    Methoden:
        interact: Führt eine Batman-spezifische Aktion aus.
    """

    def __init__(self):
        super().__init__("Batman")

    def interact(self):
        """Führt eine Batman-spezifische Aktion aus."""
        print(f"{self.name} setzt ein Bat-Gadget ein!")
