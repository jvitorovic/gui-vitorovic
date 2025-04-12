"""
Modul für die Definition von Räumen im Textadventure.

Klassen:
    Room: Basisklasse für alle Räume.
    PuzzleRoom: Repräsentiert einen Raum mit einem Rätsel.
    TrapRoom: Repräsentiert einen Raum mit einer Falle.
"""

class Room:
    """
    Basisklasse für alle Räume im Spiel.

    Attribute:
        name (str): Der Name des Raums.
        description (str): Eine Beschreibung des Raums.
        choices (dict): Die möglichen Entscheidungen und ihre Konsequenzen.
        outcomes (dict): Ergebnisse basierend auf den Entscheidungen.

    Methoden:
        resolve_choice: Verarbeitet die Auswahl des Spielers.
    """

    def __init__(self, name: str, description: str, choices: dict, outcomes: dict):
        self.name = name
        self.description = description
        self.choices = choices
        self.outcomes = outcomes

    def resolve_choice(self, choice_index: int):
        """
        Verarbeitet die Auswahl des Spielers.

        Args:
            choice_index (int): Der Index der Wahl.

        Returns:
            tuple: Ergebnis der Auswahl.
        """
        return self.outcomes.get(choice_index)


class PuzzleRoom(Room):
    """
    Repräsentiert einen Raum mit einem Rätsel.

    Attribute:
        solution (str): Die richtige Lösung für das Rätsel.

    Methoden:
        check_solution: Überprüft, ob die Lösung des Spielers korrekt ist.
    """

    def __init__(self, name: str, description: str, choices: dict, outcomes: dict, solution: str):
        super().__init__(name, description, choices, outcomes)
        self.solution = solution

    def check_solution(self, player_solution: str) -> bool:
        """
        Überprüft, ob die Lösung des Spielers korrekt ist.

        Args:
            player_solution (str): Die vom Spieler eingegebene Lösung.

        Returns:
            bool: Ob die Lösung korrekt ist.
        """
        return player_solution.lower() == self.solution.lower()


class TrapRoom(Room):
    """
    Repräsentiert einen Raum mit einer Falle.

    Attribute:
        damage (int): Der Schaden, den die Falle verursacht.

    Methoden:
        trigger_trap: Verursacht Schaden am Charakter.
    """

    def __init__(self, name: str, description: str, choices: dict, outcomes: dict, damage: int):
        super().__init__(name, description, choices, outcomes)
        self.damage = damage

    def trigger_trap(self, character):
        """
        Verursacht Schaden am Charakter.

        Args:
            character (Character): Der Charakter, der die Falle auslöst.
        """
        character.health -= self.damage
        print(f"{character.name} verliert {self.damage} Gesundheit!")
