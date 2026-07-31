import customtkinter as ctk

import settings
from data.score import ScoreManager
from ui.widgets import GameButton

import tkinter as tk
import time

from engine.background import StarField
from entities.asteroid import Asteroid


class Leaderboard(ctk.CTkFrame):

    def __init__(self, parent, back_callback):

        super().__init__(parent)

        self.configure(fg_color=settings.BACKGROUND)

        self.pack(fill="both", expand=True)

        # =====================================
        # Background Canvas
        # =====================================

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

        self.background = StarField(
            self.canvas,
            settings.WINDOW_WIDTH,
            settings.WINDOW_HEIGHT
        )

        self.asteroids = []
        self.last_spawn = 0

        self.back_callback = back_callback

        self.score_manager = ScoreManager()

        self.local_scores = self.score_manager.get_local_scores()
        

        self.build()

        self.update_background()

    # --------------------------------------------------

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
        top_bar = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=20
        )

        top_bar.grid_rowconfigure(0, weight=0, minsize=50)

        top_bar.pack(fill="x", padx=30, pady=(30, 20))
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
        ).grid(row=0, column=0, sticky="w")

        title = ctk.CTkLabel(
            top_bar,
            text="LEADERBOARD",
            font=(settings.FONT, 48),
            text_color="white"
        )

        title.grid(row=0, column=1)

        spacer = ctk.CTkLabel(
            top_bar,
            text="",
            width=170
        )

        spacer.grid(row=0, column=2)
        # ---------------- Tabs ----------------

        tab_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        tab_frame.pack(pady = (0,5))

        GameButton(
            tab_frame,
            text="LOCAL",
            width=160,
            command=lambda: None
        ).pack(side="left", padx=10)

        GameButton(
            tab_frame,
            text="GLOBAL",
            width=160,
            command=lambda: None
        ).pack(side="left", padx=10)


        # ---------------- Top Card ----------------

        if len(self.local_scores) > 0:

            best = self.local_scores[0]

        else:

            best = {
                "name": "---",
                "score": 0,
                "time": "---"
            }

        card = ctk.CTkFrame(
            self,
            fg_color="black",
            border_color="white",
            border_width=3,
            corner_radius=0,
            width=720,
            height=220
        )

        card.pack(pady=30)

        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text="#1",
            font=(settings.FONT, 42),
            text_color="white"
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            card,
            text=f"SCORE : {best['score']}",
            font=(settings.FONT, 26),
            text_color="white"
        ).pack()

        name_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        name_frame.pack(pady=8)

        ctk.CTkLabel(
            name_frame,
            text=best["name"],
            font=(settings.FONT,24),
            text_color="white"
        ).pack(side="left")

        ctk.CTkButton(
            name_frame,
            text="✎",
            width=28,
            height=28,
            fg_color="transparent",
            hover_color="#333333",
            command=lambda: self.edit_name(0)
        ).pack(side="left", padx=6)

        ctk.CTkLabel(
            card,
            text=best["time"],
            font=(settings.FONT, 18),   
            text_color="white"
        ).pack()

        # ---------------- Table ----------------

        table = ctk.CTkScrollableFrame(
            self,
            width=760,
            height=250,
            fg_color="black",
            border_color="white",
            border_width=2,
            corner_radius=0
        )

        table.pack(pady=(5,20))

        # Header

        header = ctk.CTkFrame(
            table,
            fg_color="black"
        )

        header.pack(fill="x", pady=(0, 10))

        headers = [
            ("RANK", 70),
            ("SCORE", 150),
            ("DATE", 300),
            ("NAME", 180)
        ]

        for text, width in headers:

            ctk.CTkLabel(
                header,
                text=text,
                width=width,
                anchor="center",
                font=(settings.FONT, 18),
                text_color="white"
            ).pack(side="left")

        divider = ctk.CTkFrame(
            table,
            height=2,
            fg_color="white"
        )

        divider.pack(fill="x", pady=(0, 8))

        # Rows


        if len(self.local_scores) <= 1:

            ctk.CTkLabel(
                table,
                text="NO MORE SCORES",
                font=(settings.FONT, 18),
                text_color="gray"
            ).pack(pady=20)

        else:

            for rank, score in enumerate(self.local_scores[1:], start=2):

                row = ctk.CTkFrame(
                    table,
                    fg_color="black",
                    height=35
                )

                row.pack(fill="x", pady=1)
                row.pack_propagate(False)

                # Fixed column widths
                row.grid_columnconfigure(0, minsize=70)
                row.grid_columnconfigure(1, minsize=150)
                row.grid_columnconfigure(2, minsize=300)
                row.grid_columnconfigure(3, minsize=180)

                # ---------------- Rank ----------------

                ctk.CTkLabel(
                    row,
                    text=f"#{rank}",
                    font=(settings.FONT, 16),
                    text_color="white"
                ).grid(row=0, column=0)

                # ---------------- Score ----------------

                ctk.CTkLabel(
                    row,
                    text=str(score["score"]),
                    font=(settings.FONT, 16),
                    text_color="white"
                ).grid(row=0, column=1)

                # ---------------- Date ----------------

                ctk.CTkLabel(
                    row,
                    text=score["time"],
                    font=(settings.FONT, 16),
                    text_color="white"
                ).grid(row=0, column=2)

                # ---------------- Name ----------------

                name_frame = ctk.CTkFrame(
                    row,
                    fg_color="transparent"
                )

                name_frame.grid(
                    row=0,
                    column=3
                )

                ctk.CTkLabel(
                    name_frame,
                    text=score["name"],
                    font=(settings.FONT, 16),
                    text_color="white"
                ).pack(side="left")

                ctk.CTkButton(
                    name_frame,
                    text="✎",
                    width=22,
                    height=22,
                    fg_color="transparent",
                    hover_color="#333333",
                    command=lambda i=rank-1: self.edit_name(i)
                ).pack(side="left", padx=(5, 0))

                # Divider

                ctk.CTkFrame(
                    table,
                    height=1,
                    fg_color="#404040"
                ).pack(fill="x")
        self.lift()
    # --------------------------------------------------

    def back(self):

        self.destroy()

        self.back_callback()

    def edit_name(self, index):

        popup = ctk.CTkToplevel(self)

        popup.title("Edit Name")

        popup.geometry("350x170")

        popup.resizable(False, False)

        popup.grab_set()

        ctk.CTkLabel(
            popup,
            text="Player Name",
            font=(settings.FONT, 20)
        ).pack(pady=(20,10))

        entry = ctk.CTkEntry(
            popup,
            width=220
        )

        entry.pack()

        entry.insert(0, self.local_scores[index]["name"])

        entry.focus()

        def save():

            name = entry.get().strip()

            if name == "":
                return

            self.score_manager.update_name(index, name)

            popup.destroy()

            self.destroy()

            Leaderboard(
                self.master,
                self.back_callback
            )

        ctk.CTkButton(
            popup,
            text="Save",
            command=save
        ).pack(pady=20)

        entry.bind("<Return>", lambda e: save())