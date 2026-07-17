import tkinter as tk
import customtkinter as ctk
from entities.player import Player
import settings
from engine.background import StarField

from ui.widgets import GameButton

import time

from entities.missile import Missile

class GameScreen(ctk.CTkFrame):

    def __init__(self, parent):

        self.missiles = []

        self.last_shot = 0

        super().__init__(parent)

        self.parent = parent

        self.configure(
            fg_color=settings.BACKGROUND
        )

        self.score = 0
        self.health = 3

        self.is_paused = False

        self.create_ui()
        self.update()

    # ======================================
    # UI
    # ======================================

    def create_ui(self):

        self.create_hud()
        self.create_canvas()

    # ======================================
    # HUD
    # ======================================

    def create_hud(self):

        self.hud = ctk.CTkFrame(
            self,
            height=60,
            fg_color=settings.BLACK,
            border_width=2,
            border_color=settings.WHITE,
            corner_radius=0
        )

        self.hud.pack(fill="x")
        self.hud.pack_propagate(False)

        self.score_label = ctk.CTkLabel(
            self.hud,
            text="SCORE : 000000",
            font=(settings.FONT, 18),
            text_color=settings.WHITE
        )

        self.score_label.pack(
            side="left",
            padx=20
        )

        self.pause_button = GameButton(
            self.hud,
            text="PAUSE",
            command=self.pause_game,
            width=140,
            height=40
        )

        self.pause_button.pack(
            side="right",
            padx=20,
            pady=8
        )

        self.health_label = ctk.CTkLabel(
            self.hud,
            text="❤ ❤ ❤",
            font=(settings.FONT, 18),
            text_color=settings.WHITE
        )

        self.health_label.pack(
            side="right",
            padx=20
        )

    # ======================================
    # GAME CANVAS
    # ======================================

    def create_canvas(self):

        self.canvas = tk.Canvas(

            self,

            bg="black",

            highlightthickness=0,

            width=settings.WINDOW_WIDTH,

            height=settings.WINDOW_HEIGHT - 60

        )

        self.canvas.pack(fill="both", expand=True)

        self.canvas.focus_set()
        self.background = StarField(
            self.canvas,
            settings.WINDOW_WIDTH,
            settings.WINDOW_HEIGHT - 60
        )

        self.canvas.bind("<KeyPress>", self.key_press)
        self.canvas.bind("<KeyRelease>", self.key_release)
        self.canvas.bind("<space>", self.fire_missile)
        self.player = Player(self.canvas)

    # ======================================
    # PAUSE
    # ======================================

    def pause_game(self):

        print("Pause")

    # ======================================
    # GAME LOOP
    # ======================================

    def update(self):

        if not self.is_paused:

            self.background.update()
            self.player.update()
            self.update_missiles()

        self.after(16, self.update)

    def key_press(self, event):

        key = event.keysym.lower()

        if key in ("a", "left"):
            self.player.left = True

        elif key in ("d", "right"):
            self.player.right = True

        elif key in ("w", "up"):
            self.player.up = True

        elif key in ("s", "down"):
            self.player.down = True
        
        


    def key_release(self, event):

        key = event.keysym.lower()

        if key in ("a", "left"):
            self.player.left = False

        elif key in ("d", "right"):
            self.player.right = False

        elif key in ("w", "up"):
            self.player.up = False

        elif key in ("s", "down"):
            self.player.down = False

    def fire_missile(self, event=None):

        current = time.time() * 1000

        if current - self.last_shot < settings.MISSILE_COOLDOWN:
            return

        self.last_shot = current

        x, y = self.player.get_gun_position()

        missile = Missile(
            self.canvas,
            x,
            y,
            self.player.angle
        )

        self.missiles.append(missile)

    def update_missiles(self):

        for missile in self.missiles[:]:

            missile.update()

            if missile.is_offscreen():

                missile.destroy()

                self.missiles.remove(missile)