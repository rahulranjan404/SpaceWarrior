import customtkinter as ctk

import settings
from ui.widgets import GameButton
import json
from audio import audio
import tkinter as tk
import time

from engine.background import StarField
from entities.asteroid import Asteroid

class SettingsMenu(ctk.CTkFrame):

    def __init__(self, parent, back_callback):

        super().__init__(parent)

        self.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            self,
            bg="black",
            highlightthickness=0,
            width=settings.WINDOW_WIDTH,
            height=settings.WINDOW_HEIGHT
        )

        self.canvas.place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )

        self.background = StarField(
            self.canvas,
            settings.WINDOW_WIDTH,
            settings.WINDOW_HEIGHT
        )

        self.asteroids = []
        self.last_spawn = 0

        self.soundbuttonenabled = settings.soundenabled
        self.musicbuttonenabled = settings.musicenabled
        self.build()

        self.update_background()
        self.settings_data = self.load_settings()
        
        self.back_callback = back_callback

        

    # =====================================================

    def load_settings(self):

        try:
            with open("settings.json", "r") as f:
                return json.load(f)

        except:

            return {
                "sound": True,
                "music": True
            }
    def save_settings(self):
        with open("settings.json", "w") as f:
            json.dump(self.settings_data, f, indent=4)

            # ---------------- Main Box ----------------
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
    def build(self):


        # ---------------- Top Bar ----------------

        top_bar = ctk.CTkFrame(
            self,
            fg_color="black",
            height=20
        )

        top_bar.grid_rowconfigure(
            0,
            weight=0,
            minsize=50
        )

        top_bar.pack(
            fill="x",
            padx=30,
            pady=(30, 20)
        )

        top_bar.pack_propagate(False)

        top_bar.grid_columnconfigure(0, weight=0)
        top_bar.grid_columnconfigure(1, weight=1)
        top_bar.grid_columnconfigure(2, weight=0)

        GameButton(
            top_bar,
            text="← BACK",
            width=170,
            height=45,
            command=self.back
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        title = ctk.CTkLabel(
            top_bar,
            text="SETTINGS",
            font=(settings.FONT, 48),
            text_color="white"
        )

        title.grid(
            row=0,
            column=1
        )

        spacer = ctk.CTkLabel(
            top_bar,
            text="",
            width=170
        )

        spacer.grid(
            row=0,
            column=2
        )
        box = ctk.CTkFrame(
            self,
            width=720,
            height=420,
            fg_color="black",
            border_width=3,
            border_color="white",
            corner_radius=0
        )

        box.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )
        box.pack_propagate(False)

        # =====================================================
        # AUDIO
        # =====================================================

        title = ctk.CTkLabel(
            box,
            text="AUDIO",
            font=(settings.FONT, 26),
            text_color="white"
        )

        title.pack(anchor="w", padx=35, pady=(30, 25))

        # ---------------- Sound ----------------

        sound_row = ctk.CTkFrame(
            box,
            fg_color="transparent"
        )

        sound_row.pack(fill="x", padx=35, pady=10)

        ctk.CTkLabel(
            sound_row,
            text="Sound Effects",
            font=(settings.FONT, 20),
            text_color="white"
        ).pack(side="left")

        if self.soundbuttonenabled:
            color_ = "white"
        else:
            color_ = "black"
        self.sound_box = ctk.CTkFrame(
            sound_row,
            width=24,
            height=24,
            fg_color=color_,
            border_width=2,
            border_color="white",
            corner_radius=0
        )

        self.sound_box.pack(side="right")

        self.sound_box.bind(
            "<Button-1>",
            lambda e: self.toggle_sound()
        )

        # ---------------- Music ----------------

        music_row = ctk.CTkFrame(
            box,
            fg_color="transparent"
        )



        music_row.pack(fill="x", padx=35, pady=10)

        ctk.CTkLabel(
            music_row,
            text="Music",
            font=(settings.FONT, 20),
            text_color="white"
        ).pack(side="left")

        if self.musicbuttonenabled == True:
            color_2 = "white"
        else:
            color_2 = "black"

        self.music_box = ctk.CTkFrame(
            music_row,
            width=24,
            height=24,
            fg_color=color_2,
            border_width=2,
            border_color="white",
            corner_radius=0
        )

        self.music_box.pack(side="right")

        self.music_box.bind(
            "<Button-1>",
            lambda e: self.toggle_music()
        )

        # =====================================================
        # Divider
        # =====================================================

        ctk.CTkFrame(
            box,
            height=2,
            fg_color="white"
        ).pack(fill="x", padx=30, pady=30)

        # =====================================================
        # Updates
        # =====================================================

        ctk.CTkLabel(
            box,
            text="CHECK FOR UPDATES",
            font=(settings.FONT, 26),
            text_color="white"
        ).pack(anchor="w", padx=35)

        GameButton(
            box,
            text="CHECK",
            width=200,
            command=self.check_updates
        ).pack(pady=(25, 15))

        self.update_status = ctk.CTkLabel(
            box,
            text="Status : Ready",
            font=(settings.FONT, 18),
            text_color="white"
        )

        self.update_status.pack()

    def toggle_sound(self):

        enabled = self.sound_box.cget("fg_color") == "white"

        if enabled:
            self.sound_box.configure(fg_color="black")
            settings.soundenabled = False

        else:
            self.sound_box.configure(fg_color="white")
            settings.soundenabled = True

        self.save_settings()
    # =====================================================

    def toggle_music(self):

        enabled = self.music_box.cget("fg_color") == "white"

        if enabled:
            self.music_box.configure(fg_color="black")
            settings.musicenabled = False
            audio.stop("mainmenumusic")
            
        else:
            self.music_box.configure(fg_color="white")
            settings.musicenabled = True
            audio.play_loop("mainmenumusic")
            

        self.save_settings()


    def check_updates(self):

        self.update_status.configure(
            text="Status : Loading..."
        )

        self.after(
            2000,
            lambda: self.update_status.configure(
                text="Status : Server not found."
            )
        )
    

    def make_slider(self,parent,text,value):

        row = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        row.pack(fill="x", padx=35, pady=8)

        ctk.CTkLabel(
            row,
            text=text,
            width=180,
            anchor="w",
            font=(settings.FONT,18),
            text_color="white"
        ).pack(side="left")

        slider = ctk.CTkSlider(
            row,
            from_=0,
            to=100,
            width=320
        )

        slider.pack(side="left", padx=20)
        slider.set(value)

        value_label = ctk.CTkLabel(
            row,
            text=f"{value:.0f}",
            width=40,
            font=(settings.FONT,18),
            text_color="white"
        )

        value_label.pack(side="left")

        slider.configure(
            command=lambda v,l=value_label:
                l.configure(text=f"{int(v)}")
        )

        return slider

    # =====================================================

    def control_row(self,parent,action,key):

        row = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        row.pack(fill="x", padx=35, pady=5)

        ctk.CTkLabel(
            row,
            text=action,
            width=180,
            anchor="w",
            font=(settings.FONT,18),
            text_color="white"
        ).pack(side="left")

        ctk.CTkLabel(
            row,
            text=key,
            width=120,
            font=(settings.FONT,18),
            text_color="white"
        ).pack(side="left")

        ctk.CTkButton(
            row,
            text="✎",
            width=35,
            height=30,
            fg_color="transparent",
            hover_color="#333333"
        ).pack(side="left")

    # =====================================================

    def separator(self,parent):

        ctk.CTkFrame(
            parent,
            height=2,
            fg_color="white"
        ).pack(fill="x", padx=25, pady=18)

    # =====================================================

    def save(self):

        print("Sound:", int(self.sound_slider.get()))
        print("Music:", int(self.music_slider.get()))
        print("Mouse:", int(self.mouse_slider.get()))

    # =====================================================

    def back(self):

        self.destroy()

        self.back_callback()