# Für die Geschichten der Json Files ist eine KI verwendet worden

"""
Das Hauptmodul für das Textadventure-Spiel. Es verwaltet den Spielablauf, die Charakterauswahl und die Interaktionen
zwischen den Räumen und dem Spieler.

Klassen:
    GameManager: Verwaltet den Spielablauf und die Steuerung.

Funktionen:
    validate_input: Validiert die Eingabe des Benutzers.
    create_room: Erstellt eine Instanz der passenden Raumklasse basierend auf JSON-Daten.
"""

import json
from characters.batman import Batman
from characters.joker import Joker
from rooms.room import Room, PuzzleRoom, TrapRoom
from utils.print_slow import PrintSlow
from gui import TextAdventureApp

def validate_input(prompt: str, valid_options: list) -> str:
    """
    Validiert die Benutzereingabe, bis eine gültige Option eingegeben wird.

    Args:
        prompt (str): Die Eingabeaufforderung, die dem Benutzer angezeigt wird.
        valid_options (list): Liste gültiger Optionen, die der Benutzer wählen kann.

    Returns:
        str: Die gültige Eingabe des Benutzers.
    """
    while True:
        choice = input(prompt).lower().strip()
        if choice in valid_options:
            return choice
        print("Ungültige Eingabe, bitte erneut versuchen.")


def create_room(data: dict):
    """
    Erstellt eine Instanz der passenden Raumklasse basierend auf den JSON-Daten.

    Args:
        data (dict): Die Raumdaten aus der JSON-Datei.

    Returns:
        Room: Eine Instanz der entsprechenden Raumklasse.
    """
    room_type = data.get("room_type", "Room")
    name = data.get("name", "Unbekannter Raum")
    description = data.get("description", "Keine Beschreibung vorhanden.")
    choices = data.get("choices", {})
    outcomes = data.get("outcomes", {})

    if room_type == "PuzzleRoom":
        solution = data.get("solution", "Keine Lösung definiert.")
        return PuzzleRoom(name, description, choices, outcomes, solution)
    elif room_type == "TrapRoom":
        damage = data.get("damage", 0)
        return TrapRoom(name, description, choices, outcomes, damage)
    else:
        return Room(name, description, choices, outcomes)


class GameManager:
    """
    Verwalter für das gesamte Spiel. Steuert den Ablauf, die Charakterauswahl und den Fortschritt des Spielers.

    Methoden:
        choose_character: Lässt den Spieler einen Charakter wählen und lädt das Abenteuer.
        load_adventure: Lädt Abenteuerdaten aus einer JSON-Datei.
        play: Startet das Spiel und steuert den Fortschritt.
    """

    def __init__(self):
        """
        Initialisiert die GameManager-Klasse.
        """
        self.character = None
        self.rooms = None
        self.current_room_id = "1"
        self.printer = PrintSlow()

    def choose_character(self):
        """
        Lässt den Spieler einen Charakter wählen und lädt die entsprechende Abenteuerdatei.
        """
        self.printer.print("Willkommen im Textadventure!")
        self.printer.print("Wähle deinen Charakter:")
        print("1) Batman")
        print("2) Joker")

        choice = validate_input("Gib die Nummer deines Charakters ein: ", ["1", "2"])

        if choice == "1":
            self.character = Batman()
            self.load_adventure("adventures/batman_adventure.json")
        elif choice == "2":
            self.character = Joker()
            self.load_adventure("adventures/joker_adventure.json")

    def load_adventure(self, file_path):
        """
        Lädt die Abenteuer-Daten aus einer JSON-Datei.

        Args:
            file_path (str): Pfad zur JSON-Datei.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                raw_data = json.load(file)
                self.rooms = {key: create_room(value) for key, value in raw_data.items()}
        except FileNotFoundError:
            print(f"Fehler: Die Datei {file_path} wurde nicht gefunden.")
            exit(1)
        except json.JSONDecodeError:
            print(f"Fehler: Die Datei {file_path} enthält ungültiges JSON.")
            exit(1)

    def play(self):
        """
        Startet das Spiel und steuert den Fortschritt durch die Räume.
        """
        self.choose_character()
        self.printer.print(f"Du spielst als {self.character.name}.")

        while self.current_room_id and self.character.is_alive():
            current_room = self.rooms.get(self.current_room_id)
            if not current_room:
                print(f"Fehler: Raum {self.current_room_id} wurde nicht gefunden.")
                break

            self.printer.print(f"\nRaum: {current_room.name}")
            self.printer.print(current_room.description)

            for key, choice in current_room.choices.items():
                print(f"{key}) {choice[0]}")

            user_input = validate_input("Wähle eine Option: ", current_room.choices.keys())
            self.current_room_id = current_room.choices[user_input][1]


#if __name__ == "__main__":
 #   game = GameManager()
  #  game.play()


if __name__ == "__main__":
    app = TextAdventureApp()
    app.mainloop()