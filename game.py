import tkinter as tk
import customtkinter as ctk
from entities.player import Player
import settings
from engine.background import StarField
import pygame
from score import ScoreManager

from entities.explosion import Explosion

from ui.gameover import GameOverMenu

from collision import circle_collision

from ui.widgets import GameButton

from audio import audio
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

        self.last_survival_score = time.time() * 1000

        self.game_time = 0
        self.speed_multiplier = 1.0



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

        # self.health_label = ctk.CTkLabel(
        #     self.hud,
        #     text="❤ ❤ ❤",
        #     font=(settings.FONT, 18),
        #     text_color=settings.WHITE
        # )

        # self.health_label.pack(
        #     side="right",
        #     padx=20
        # )

    # ======================================
    # GAME CANVAS
    # ======================================
        audio.play_loop("alive")

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

       

        if self.is_paused:

            self.resume_game()
        else:
            self.show_pause_menu()

    def show_pause_menu(self):

        self.is_paused = True
        pygame.mixer.pause()
        self.pause_button.configure(text="RESUME")

        # Dark overlay
        # self.pause_overlay = ctk.CTkFrame(
        #     self,
        #     fg_color="transparent"
        # )

        # self.pause_overlay.place(
        #     relx=0,
        #     rely=0,
        #     relwidth=1,
        #     relheight=1
        # )

        # Center box
        
        self.box = ctk.CTkFrame(
            self.canvas,
            width=500,
            height=430,
            fg_color="black",
            border_width=3,
            border_color="white",
            corner_radius=0
        )
        box = self.box
        box.place(relx=0.5, rely=0.5, anchor="center")
        box.pack_propagate(False)

        # Title
        ctk.CTkLabel(
            box,
            text="PAUSED",
            font=(settings.FONT, 42),
            text_color="white"
        ).pack(pady=(40, 35))

        # Score
        ctk.CTkLabel(
            box,
            text=f"SCORE : {self.score_manager.score}",
            font=(settings.FONT, 24),
            text_color="white"
        ).pack(pady=8)

        # Highscore
        ctk.CTkLabel(
            box,
            text=f"HIGH SCORE : {self.score_manager.get_best_score()['score']}",
            font=(settings.FONT, 24),
            text_color="white"
        ).pack(pady=(0, 40))

        # Resume
        GameButton(
            box,
            text="RESUME",
            width=240,
            command=self.resume_game
        ).pack(pady=8)

        # Exit
        GameButton(
            box,
            text="EXIT",
            width=240,
            command=self.exit_game
        ).pack(pady=8)

    def resume_game(self):

        self.is_paused = False
        pygame.mixer.unpause()
        self.pause_button.configure(text="PAUSE")

        self.box.destroy()


    def update(self):

        if not self.is_paused:

            # ~60 FPS
            self.game_time += 1

            # Increase slowly over time (max 3x)
            self.speed_multiplier = min(
                2.5,
                1 + self.game_time / 6000
            )

            self.background.speed_multiplier = self.speed_multiplier

            self.background.update()

            self.player.update()

            self.update_missiles()

            self.spawn_asteroid()

            self.update_asteroids()

            self.check_collisions()

            self.check_player_collision()

            self.update_survival_score()

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
        
        audio.play("shoot")
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

        # Spawn delay decreases as difficulty increases
        spawn_delay = settings.ASTEROID_SPAWN_DELAY / self.speed_multiplier

        # Don't let it become ridiculously fast
        spawn_delay = max(180, spawn_delay)

        if current - self.last_asteroid_spawn < spawn_delay:
            return

        self.last_asteroid_spawn = current

        self.asteroids.append(
            Asteroid(self.canvas)
        )

    def update_asteroids(self):

        for asteroid in self.asteroids[:]:

            asteroid.speed_multiplier = self.speed_multiplier
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

                audio.stop("alive")
                audio.play("explosion")
                
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

        self.score_manager.save_local_score("PLAYER")

        bestscore = self.score_manager.get_best_score()
        # self.game_over_menu = GameOverMenu(
        #     self,
        #     restart_callback=self.restart_game,
        #     exit_callback=self.exit_game,
        #     score=self.score_manager.score,
        #     highscore=bestscore
        # )
        # self.game_over_menu.place(
        #     relx=0.5,
        #     rely=0.5,
        #     anchor="center",
        #     relwidth=1,
        #     relheight=1
        # )

        self.hud.pack_forget()
        score=self.score_manager.score
        highscore=bestscore
        self.panel = ctk.CTkFrame(
                    self,
                    width=420,
                    height=360,
                    fg_color=settings.BLACK,
                    border_width=2,
                    border_color=settings.WHITE,
                    corner_radius=0
                )
        
        self.panel.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )   

        panel = self.panel

        panel.pack_propagate(False)

        title = ctk.CTkLabel(
            panel,
            text="GAME OVER",
            font=(settings.FONT, 42),
            text_color=settings.WHITE
        )
        title.pack(pady=(40, 40))

        score_label = ctk.CTkLabel(
            panel,
            text=f"SCORE : {score}",
            font=(settings.FONT, 20),
            text_color=settings.WHITE
        )
        score_label.pack(pady=(0, 8))

        highscore_label = ctk.CTkLabel(
            panel,
            text=f"HIGH SCORE : {highscore['score']}",
            font=(settings.FONT, 20),
            text_color=settings.WHITE
            )
        highscore_label.pack(pady=(0, 25))

        

        GameButton(
            panel,
            text="RESTART",
            command=self.restart_game,
            width=220,
            height=45
        ).pack(pady=10)

        GameButton(
            panel,
            text="EXIT",
            command=self.exit_game,
            width=220,
            height=45
        ).pack(pady=10)
    
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

    def update_survival_score(self):

        current = time.time() * 1000

        while current - self.last_survival_score >= 200:

            self.score_manager.add(1)

            self.last_survival_score += 200

        self.update_score()