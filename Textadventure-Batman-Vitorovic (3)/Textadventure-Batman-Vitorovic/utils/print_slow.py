"""
Modul für langsame Textausgabe.

Klassen:
    PrintSlow: Verwaltet die langsame Ausgabe von Text auf der Konsole.
"""

import time

class PrintSlow:
    """
    Klasse für langsame Textausgabe.

    Attribute:
        delay (float): Verzögerung in Sekunden pro Zeichen.

    Methoden:
        print: Gibt Text Zeichen für Zeichen mit einer Verzögerung aus.
        set_delay: Setzt eine neue Verzögerung.
        print_instant (static): Gibt Text ohne Verzögerung aus.
    """

    def __init__(self, delay: float = 0.05):
        self.delay = delay

    def print(self, text: str):
        """
        Gibt Text Zeichen für Zeichen mit einer Verzögerung aus.

        Args:
            text (str): Der auszugebende Text.
        """
        for char in text:
            print(char, end="", flush=True)
            time.sleep(self.delay)
        print()

    def set_delay(self, new_delay: float):
        """
        Setzt eine neue Verzögerung.

        Args:
            new_delay (float): Die neue Verzögerung in Sekunden.
        """
        self.delay = new_delay

    @staticmethod
    def print_instant(text: str):
        """
        Gibt Text ohne Verzögerung aus.

        Args:
            text (str): Der auszugebende Text.
        """
        print(text)
