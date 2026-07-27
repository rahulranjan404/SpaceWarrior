import customtkinter as ctk

import settings
from game import GameScreen

from ui.widgets import GameButton


class MainMenu(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.configure(
            fg_color=settings.BACKGROUND
        )

        self.create_widgets()

    def create_widgets(self):

        container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        container.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # -----------------------
        # Title
        # -----------------------

        title = ctk.CTkLabel(

            container,

            text="SPACE WARRIOR",

            font=(
                settings.FONT,
                settings.TITLE_SIZE
            ),

            text_color=settings.WHITE,

            justify="center"
        )

        title.pack(pady=(0, 15))

        subtitle = ctk.CTkLabel(

            container,

            text="- ENDLESS SPACE BATTLE -",

            font=(
                settings.FONT,
                settings.SUBTITLE_SIZE
            ),

            text_color=settings.WHITE

        )

        subtitle.pack(pady=(0, 50))

        # -----------------------
        # Buttons
        # -----------------------

        GameButton(
            container,
            "PLAY",
            self.play_game
        ).pack(pady=8)

        GameButton(
            container,
            "HIGH SCORES",
            self.high_scores
        ).pack(pady=8)

        GameButton(
            container,
            "SETTINGS",
            self.settings
        ).pack(pady=8)

        GameButton(
            container,
            "EXIT",
            self.parent.destroy
        ).pack(pady=8)

        version = ctk.CTkLabel(

            self,

            text="v1.0",

            text_color=settings.WHITE,

            font=(
                settings.FONT,
                12
            )

        )

        version.place(
            relx=0.98,
            rely=0.98,
            anchor="se"
        )

    def play_game(self):
        self.parent.change_screen(GameScreen)

    def high_scores(self):
        print("High Scores")
        self.open_leaderboard()

    def settings(self):
        print("Settings")

    def open_leaderboard(self):

        self.destroy()

        from ui.leaderboard import Leaderboard

        Leaderboard(
            self.parent,
            self.parent.show_menu
        )