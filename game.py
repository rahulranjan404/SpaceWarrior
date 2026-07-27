import tkinter as tk
import customtkinter as ctk
from entities.player import Player
import settings
from engine.background import StarField

from score import ScoreManager

from entities.explosion import Explosion

from ui.gameover import GameOverMenu

from collision import circle_collision

from ui.widgets import GameButton

import time
import random

from entities.asteroid import Asteroid


from entities.missile import Missile

class GameScreen(ctk.CTkFrame):

    def __init__(self, parent):

        self.missiles = []

        self.last_shot = 0

        self.asteroids = []

        self.explosions = []

        self.last_asteroid_spawn = 0

        self.pending_game_over = False

        self.player_explosion = None

        self.score_manager = ScoreManager()



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

            self.spawn_asteroid()

            self.update_asteroids()

            self.check_collisions()

            self.check_player_collision()

        self.update_explosions()

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

    def spawn_asteroid(self):

        current = time.time() * 1000

        if (
            current - self.last_asteroid_spawn
            < settings.ASTEROID_SPAWN_DELAY
        ):
            return

        self.last_asteroid_spawn = current

        self.asteroids.append(
            Asteroid(self.canvas)
        )

    def update_asteroids(self):

        for asteroid in self.asteroids[:]:

            asteroid.update()

            if asteroid.is_offscreen():

                asteroid.destroy()

                self.asteroids.remove(asteroid)

    def check_collisions(self):

        for missile in self.missiles[:]:

            missile_x, missile_y = self.canvas.coords(
                missile.sprite
            )
            missile_x, missile_y = self.canvas.coords(missile.sprite)

           
            for asteroid in self.asteroids[:]:

                
                
                asteroid_x, asteroid_y = self.canvas.coords(
                    asteroid.sprite
                )


                if circle_collision(

                    missile_x,
                    missile_y,
                    missile.radius,

                    asteroid_x,
                    asteroid_y,
                    asteroid.radius

                ):
                    asteroid.apply_knockback(
                            missile.vx*0.2,
                            missile.vy*0.2
                        )
                    self.create_explosion(
                    asteroid_x,
                    asteroid_y,
                    "impact",
                    40
                )

                    missile.destroy()
                    self.missiles.remove(missile)

                    destroyed = asteroid.take_damage()

                    if destroyed:

                        self.create_explosion(
                        asteroid_x,
                        asteroid_y,
                        "destroy",
                        asteroid.size
                    )
                        if asteroid.size <= 60:
                            points = 10

                        elif asteroid.size <= 75:
                            points = 20

                        else:
                            points = 40

                        self.score_manager.add(points)

                        self.update_score()

                    
                        asteroid.destroy()

                        self.asteroids.remove(asteroid)

                    break

    def check_player_collision(self):

        player_x = self.player.x
        player_y = self.player.y

        for asteroid in self.asteroids[:]:

            asteroid_x, asteroid_y = self.canvas.coords(
                asteroid.sprite
            )

            if circle_collision(

                player_x,
                player_y,
                self.player.radius,

                asteroid_x,
                asteroid_y,
                asteroid.radius

            ):
                # Freeze gameplay
                self.is_paused = True

                # Remove player sprite
                self.canvas.delete(self.player.sprite)

                # Create explosion
                self.player_explosion = self.create_explosion(
                    player_x,
                    player_y,
                    "destroy",
                    110
                )

                self.pending_game_over = True

                return

    def show_game_over(self):

        self.score_manager.save_highscore()

        self.game_over_menu = GameOverMenu(
            self,
            restart_callback=self.restart_game,
            exit_callback=self.exit_game,
            score=self.score_manager.score,
            highscore=self.score_manager.highscore
        )
    
    def restart_game(self):

        self.destroy()

        from game import GameScreen

        game = GameScreen(self.parent)

        game.pack(fill="both", expand=True)


    def exit_game(self):

        self.destroy()

        self.parent.show_menu()

    def create_explosion(self, x, y, explosion_type="impact", size=64):

        explosion = Explosion(
            self.canvas,
            x,
            y,
            explosion_type,
            size
        )

        self.explosions.append(explosion)

        return explosion

    def update_explosions(self):

        for explosion in self.explosions[:]:

            explosion.update()

            if explosion.finished:

                if explosion == self.player_explosion and self.pending_game_over:

                    self.pending_game_over = False

                    self.show_game_over()

                self.explosions.remove(explosion)

    def update_score(self):

        self.score_label.configure(
            text=f"SCORE : {self.score_manager.score}"
    )