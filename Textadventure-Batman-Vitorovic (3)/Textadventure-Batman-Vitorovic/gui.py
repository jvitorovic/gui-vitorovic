# Importiert benötigte Module
import customtkinter as ctk  
from tkinter import messagebox, scrolledtext  
from PIL import Image  
import json, os, sys  

# Setze das Erscheinungsbild der GUI (Dark Mode) und Farbthema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Hauptklasse der Anwendung, erbt von CTk (Hauptfenster)
class TextAdventureApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Batman Textadventure")
        self.geometry("1000x700")          # Startgröße des Fensters
        self.minsize(800, 600)             # Mindestgröße
        self.font_size = 17                # Standard-Schriftgröße
        self.current_frame = None          # Aktuell angezeigter Frame
        self.adventure_data = {}           # Hier werden die Szenendaten geladen
        self.bind("<Configure>", self.on_resize)  # Bei Größenänderung → Schrift anpassen
        self.show_start_screen()           # Starte mit dem Startbildschirm

    # Zeigt den Startbildschirm zur Charakterwahl
    def show_start_screen(self):
        self.clear_current_frame()

        frame = ctk.CTkFrame(self, corner_radius=20)
        frame.pack(expand=True)

        # Titel und Anweisung
        ctk.CTkLabel(frame, text="🦇 Batman Textadventure", font=("Segoe UI", self.font_size + 12, "bold")).pack(pady=20)
        ctk.CTkLabel(frame, text="Wähle deinen Charakter:", font=("Segoe UI", self.font_size + 2)).pack(pady=10)

        # Buttons zur Charakterwahl
        ctk.CTkButton(
            frame, text="🦇 Batman", font=("Segoe UI", self.font_size),
            fg_color="transparent", hover_color="#1E88E5",
            command=lambda: self.start_game("batman"), corner_radius=10
        ).pack(pady=6)

        ctk.CTkButton(
            frame, text="🤡 Joker", font=("Segoe UI", self.font_size),
            fg_color="transparent", hover_color="#E53935",
            command=lambda: self.start_game("joker"), corner_radius=10
        ).pack(pady=6)

        self.current_frame = frame

    # Startet das Spiel mit dem gewählten Charakter
    def start_game(self, character_name):
        path = os.path.join("adventures", f"{character_name}_adventure.json")

        if not os.path.exists(path):
            messagebox.showerror("Fehler", f"Datei nicht gefunden: {path}")
            self.show_start_screen()
            return

        with open(path, "r", encoding="utf-8") as f:
            self.adventure_data = json.load(f)

        self.clear_current_frame()
        self.current_frame = GameScreen(self, self.adventure_data, character_name, self.font_size)
        self.current_frame.pack(fill="both", expand=True)

    # Entfernt den aktuell angezeigten Frame
    def clear_current_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    # Reagiert auf Fenstergrößenänderung und passt Schriftgröße an
    def on_resize(self, event):
        neue_fontgroesse = max(12, int(event.height / 50))
        if neue_fontgroesse != self.font_size:
            self.font_size = neue_fontgroesse
            if hasattr(self.current_frame, "update_font"):
                self.current_frame.update_font(self.font_size)

# Klasse für den Spielbildschirm
class GameScreen(ctk.CTkFrame):
    def __init__(self, master, adventure_data, character_name, font_size):
        super().__init__(master)
        self.adventure_data = adventure_data
        self.character_name = character_name
        self.font_size = font_size
        self.current_scene_id = "1"
        self.total_scenes = len([k for k in adventure_data.keys() if k.isdigit()])
        self._print_cancelled = False

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        info = self.adventure_data.get("start", {})
        self.sidebar = self.build_sidebar(info)
        self.sidebar.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        self.main = ctk.CTkFrame(self, corner_radius=15)
        self.main.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Textbox für die Geschichte – leicht vergrößert (height=18)
        self.story_box = scrolledtext.ScrolledText(
            self.main, wrap="word", font=("Consolas", font_size),
            height=18, bg="#1a1a1a", fg="#ffffff", borderwidth=0
        )
        self.story_box.pack(fill="x", pady=(0, 10))
        self.story_box.configure(state="disabled")

        # Fortschrittsanzeige
        self.progress_frame = ctk.CTkFrame(self.main)
        self.progress_frame.pack(fill="x", pady=(0, 10))
        self.progress = ctk.CTkProgressBar(self.progress_frame, height=20)
        self.progress.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.progress_text = ctk.CTkLabel(self.progress_frame, text="0 %", font=("Segoe UI", self.font_size - 2))
        self.progress_text.pack(side="right")

        # Auswahlbereich
        self.choice_area = ctk.CTkFrame(self.main, corner_radius=10)
        self.choice_area.pack(fill="x")

        # Szenenstatus
        self.status_label = ctk.CTkLabel(
            self.main,
            text=f"Szene: {self.current_scene_id} | Charakter: {self.character_name.capitalize()}",
            font=("Segoe UI", self.font_size - 2),
            text_color="#888888"
        )
        self.status_label.pack(pady=(10, 0))

        # Menü- und Beenden-Buttons
        ctk.CTkButton(self.main, text="🔙 Zurück zum Menü", command=self.master.show_start_screen,
                      fg_color="transparent", hover_color="#455A64", font=("Segoe UI", self.font_size - 1),
                      corner_radius=8).pack(pady=(20, 4))

        ctk.CTkButton(self.main, text="❌ Beenden", command=self.master.destroy,
                      fg_color="transparent", hover_color="#B71C1C", font=("Segoe UI", self.font_size - 1),
                      corner_radius=8).pack(pady=(0, 10))

        self.show_scene(self.current_scene_id)

    # Erstellt die linke Sidebar mit Infos und Bild
    def build_sidebar(self, info):
        frame = ctk.CTkFrame(self, width=260, corner_radius=15)
        frame.pack_propagate(False)

        ctk.CTkLabel(frame, text="Charakter", font=("Segoe UI", self.font_size + 2, "bold")).pack(pady=(10, 0))
        ctk.CTkLabel(frame, text=info.get("character_overview", ""), wraplength=240, justify="left",
                     font=("Segoe UI", self.font_size)).pack(pady=10)

        ctk.CTkLabel(frame, text="Ziel", font=("Segoe UI", self.font_size + 2, "bold")).pack(pady=(20, 0))
        ctk.CTkLabel(frame, text=info.get("objective", ""), wraplength=240, justify="left",
                     font=("Segoe UI", self.font_size)).pack(pady=10)

        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        image_path = os.path.join(script_dir, "assets", f"{self.character_name}.jpg")

        if os.path.exists(image_path):
            img = Image.open(image_path).resize((240, 320))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(240, 320))
            img_label = ctk.CTkLabel(frame, image=ctk_img, text="", corner_radius=12)
            img_label.image = ctk_img
            img_label.pack(pady=12, anchor="center")
        else:
            ctk.CTkLabel(frame, text=f"[Bild nicht gefunden: {image_path}]", font=("Segoe UI", 10, "italic")).pack(pady=10)

        return frame

    # Zeigt die Szene + Entscheidungsoptionen
    def show_scene(self, scene_id):
        self._print_cancelled = True
        self.current_scene_id = scene_id
        scene = self.adventure_data.get(scene_id, {})
        text = f"{scene.get('name', '')}\n\n{scene.get('description', '')}"
        self.print_slow_gui(text)

        for widget in self.choice_area.winfo_children():
            widget.destroy()

        for key, (desc, next_id) in scene.get("choices", {}).items():
            ctk.CTkButton(self.choice_area, text=f"{key.upper()}: {desc}", font=("Segoe UI", self.font_size),
                          corner_radius=8, fg_color="#263238", hover_color="#37474F",
                          command=lambda nid=next_id: self.show_scene(nid)).pack(pady=6, padx=20, fill="x")

        try:
            progress_value = int(scene_id) / self.total_scenes
            self.progress.set(progress_value)
            self.progress_text.configure(text=f"{int(progress_value * 100)} %")
        except:
            self.progress.set(0)
            self.progress_text.configure(text="0 %")

        self.status_label.configure(text=f"Szene: {self.current_scene_id} | Charakter: {self.character_name.capitalize()}")

    # Gibt Text mit Schreibmaschineneffekt aus
    def print_slow_gui(self, text, delay=10):
        self.story_box.configure(state="normal")
        self.story_box.delete("1.0", "end")
        self._print_cancelled = False

        def type_writer(index=0):
            if self._print_cancelled:
                self.story_box.configure(state="disabled")
                return
            if index < len(text):
                self.story_box.insert("end", text[index])
                self.story_box.see("end")
                self.after(delay, lambda: type_writer(index + 1))
            else:
                self.story_box.configure(state="disabled")

        type_writer()

    # Aktualisiert Schriftgröße bei Resize
    def update_font(self, new_size):
        self.font_size = new_size
        self.story_box.configure(font=("Consolas", self.font_size))
        for widget in self.choice_area.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(font=("Segoe UI", self.font_size))

# Hinweis: Der Text der Szene sollte zuerst komplett angezeigt werden,
# erst danach sollen die Entscheidungsoptionen getroffen werden.
