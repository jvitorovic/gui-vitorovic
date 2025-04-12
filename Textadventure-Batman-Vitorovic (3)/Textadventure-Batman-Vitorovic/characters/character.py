"""
Modul für die Definition von Charakteren im Spiel.

Klassen:
    Character: Basisklasse für alle Charaktere.
"""

class Character:
    """
    Basisklasse für alle Charaktere im Spiel. Definiert grundlegende Attribute und Methoden für Spieler und NPCs.

    Attribute:
        name (str): Der Name des Charakters.
        _health (int): Die aktuelle Gesundheit des Charakters.
        _inventory (list): Das Inventar des Charakters.

    Methoden:
        health (property): Gibt die aktuelle Gesundheit zurück oder setzt sie.
        add_to_inventory: Fügt ein Item zum Inventar hinzu.
        is_alive: Überprüft, ob der Charakter noch lebt.
        interact: Abstrakte Methode, die von abgeleiteten Klassen implementiert wird.
        create_standard_characters (static): Erstellt eine Liste vordefinierter Charaktere.
    """

    @staticmethod
    def create_standard_characters():
        """
        Erstellt eine Liste von Standardcharakteren.

        Returns:
            list: Eine Liste vordefinierter Charakterinstanzen.
        """
        from characters.batman import Batman
        from characters.joker import Joker
        return [Batman(), Joker()]

    def __init__(self, name: str):
        self.name = name
        self._health = 100
        self._inventory = []

    @property
    def health(self) -> int:
        """Ruft die aktuelle Gesundheit des Charakters ab."""
        return self._health

    @health.setter
    def health(self, value: int):
        """Setzt die Gesundheit des Charakters, begrenzt auf 0-100."""
        self._health = max(0, min(value, 100))

    def add_to_inventory(self, item: str):
        """Fügt ein Item zum Inventar hinzu."""
        self._inventory.append(item)

    def is_alive(self) -> bool:
        """Prüft, ob der Charakter noch lebt."""
        return self._health > 0

    def interact(self):
        """Interaktion, die von abgeleiteten Klassen implementiert wird."""
        raise NotImplementedError("Diese Methode muss überschrieben werden.")
