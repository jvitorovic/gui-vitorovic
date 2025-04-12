"""
Modul für die Definition des Joker-Charakters.

Klassen:
    Joker: Abgeleitete Klasse, die Joker als spielbaren Charakter repräsentiert.
"""

from characters.character import Character

class Joker(Character):
    """
    Repräsentiert Joker als spielbaren Charakter.

    Methoden:
        interact: Führt eine Joker-spezifische Aktion aus.
    """

    def __init__(self):
        super().__init__("Joker")

    def interact(self):
        """Führt eine Joker-spezifische Aktion aus."""
        print(f"{self.name} lacht böse und spielt einen Trick!")
