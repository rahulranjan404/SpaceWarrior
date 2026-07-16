import customtkinter as ctk


class MainMenu(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        # Background
        self.configure(fg_color="#0B1020")

        self.create_widgets()

    def create_widgets(self):

        # ======================
        # Title
        # ======================

        title = ctk.CTkLabel(
            self,
            text="SPACE WARRIOR",
            font=("Arial", 42, "bold"),
            text_color="#FFFFFF"
        )

        title.pack(pady=(80, 10))

        subtitle = ctk.CTkLabel(
            self,
            text="Endless Space Battle",
            font=("Arial", 18),
            text_color="#A0A0A0"
        )

        subtitle.pack(pady=(0, 50))

        # ======================
        # Buttons
        # ======================

        play_button = ctk.CTkButton(
            self,
            text="PLAY",
            width=250,
            height=45,
            command=self.play_game
        )

        play_button.pack(pady=10)

        highscore_button = ctk.CTkButton(
            self,
            text="HIGH SCORES",
            width=250,
            height=45,
            command=self.show_highscores
        )

        highscore_button.pack(pady=10)

        settings_button = ctk.CTkButton(
            self,
            text="SETTINGS",
            width=250,
            height=45,
            command=self.open_settings
        )

        settings_button.pack(pady=10)

        exit_button = ctk.CTkButton(
            self,
            text="EXIT",
            width=250,
            height=45,
            fg_color="#C0392B",
            hover_color="#922B21",
            command=self.parent.destroy
        )

        exit_button.pack(pady=10)

    def play_game(self):
        print("Play Game")

    def show_highscores(self):
        print("High Scores")

    def open_settings(self):
        print("Settings")