import tkinter as tk
import customtkinter as ctk
import time
import ui.settingsmenu as settingsmenu
import settings
from engine.audio import audio
from game import GameScreen
from ui.widgets import GameButton

from engine.background import StarField
from entities.asteroid import Asteroid



class MainMenu(ctk.CTkFrame):

    audio.load(
            "mainmenumusic",
            "assets/music/music1.mp3"
        )


    def __init__(self, parent):

        super().__init__(parent)

        self.parent = parent

        self.configure(
            fg_color=settings.BACKGROUND
        )

        # ==================================================
        # BACKGROUND CANVAS
        # ==================================================

        self.canvas = tk.Canvas(
            self,
            width=settings.WINDOW_WIDTH,
            height=settings.WINDOW_HEIGHT,
            bg="black",
            highlightthickness=0
        )

        self.canvas.place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )
        self.mainmenumsuic = settings.mainmusicbool
        # Animated background

        self.background = StarField(
            self.canvas,
            settings.WINDOW_WIDTH,
            settings.WINDOW_HEIGHT
        )

        self.asteroids = []
        self.last_spawn = 0

        # UI

        self.create_widgets()
        self.playmusic()

        # Start animation

        self.update_background()
        
    # ==================================================

    def playmusic(self):
        print(self.mainmenumsuic)
        if self.mainmenumsuic == False:
            settings.mainmusicbool = True
            print("Playing main menu music")
            audio.play_loop("mainmenumusic")
        else:
            pass
    def create_widgets(self):

        # ----------------------------
        # TITLE
        # ----------------------------

        title = ctk.CTkLabel(
            self,
            text="SPACE WARRIOR",
            font=(settings.FONT, settings.TITLE_SIZE),
            text_color=settings.WHITE,
            fg_color="transparent"
        )

        title.place(
            relx=0.5,
            rely=0.20,
            anchor="center"
        )

        subtitle = ctk.CTkLabel(
            self,
            text="- ENDLESS SPACE BATTLE -",
            font=(settings.FONT, settings.SUBTITLE_SIZE),
            text_color=settings.WHITE,
            fg_color="transparent"
        )

        subtitle.place(
            relx=0.5,
            rely=0.26,
            anchor="center"
        )

        # ----------------------------
        # BUTTON BOX
        # ----------------------------

        self.container = ctk.CTkFrame(
            self,
            width=370,
            height=320,
            fg_color="black",
            border_width=2,
            border_color="white",
            corner_radius=0
        )

        self.container.place(
            relx=0.5,
            rely=0.58,
            anchor="center"
        )

        self.container.pack_propagate(False)

        # ----------------------------
        # BUTTONS
        # ----------------------------

        GameButton(
            self.container,
            "PLAY",
            self.play_game,
            style="default"
        ).pack(pady=(15, 8))

        GameButton(
            self.container,
            "HIGH SCORES",
            self.high_scores,
            style="default"
        ).pack(pady=8)

        GameButton(
            self.container,
            "SETTINGS",
            self.settings,
            style="default"
        ).pack(pady=8)

        GameButton(
            self.container,
            "EXIT",
            self.parent.destroy,
            style="default"
        ).pack(pady=(8,15))

        # ----------------------------
        # VERSION
        # ----------------------------

        version = ctk.CTkLabel(
            self,
            text="v1.0",
            font=(settings.FONT, 12),
            text_color=settings.WHITE,
            fg_color="transparent"
        )

        version.place(
            relx=0.985,
            rely=0.985,
            anchor="se"
        )

    # ==================================================

    def update_background(self):

        self.background.update()

        current = time.time()

        if current - self.last_spawn > 2:

            asteroid = Asteroid(self.canvas)

            asteroid.rotation_speed *= 0.5

            self.asteroids.append(asteroid)

            self.last_spawn = current

        for asteroid in self.asteroids[:]:

            asteroid.update()

            if asteroid.is_offscreen():

                asteroid.destroy()

                self.asteroids.remove(asteroid)

        self.after(16, self.update_background)

    # ==================================================

    def play_game(self):

        audio.stop("mainmenumusic")
        settings.mainmusicbool = False
        self.parent.change_screen(GameScreen)

    def high_scores(self):

        self.destroy()

        from ui.leaderboard import Leaderboard

        Leaderboard(
            self.parent,
            self.parent.show_menu
        )

    def settings(self):
        self.destroy()
        settingsmenu.SettingsMenu(self.parent, self.parent.show_menu)
        print("Settings")