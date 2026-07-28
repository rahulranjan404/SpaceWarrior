import customtkinter as ctk

import settings
from score import ScoreManager
from ui.widgets import GameButton


class Leaderboard(ctk.CTkFrame):

    def __init__(self, parent, back_callback):

        super().__init__(parent)

        self.configure(fg_color=settings.BACKGROUND)

        self.pack(fill="both", expand=True)

        self.back_callback = back_callback

        self.score_manager = ScoreManager()

        self.local_scores = self.score_manager.get_local_scores()

        self.build()

    # --------------------------------------------------

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

        ctk.CTkLabel(
            card,
            text=best["name"],
            font=(settings.FONT, 24),
            text_color="white"
        ).pack(pady=8)

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

        table.pack(pady=20)

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
                    fg_color="black"
                )

                row.pack(fill="x", pady=2)

                values = [
                    f"#{rank}",
                    str(score["score"]),
                    score["time"],
                    score["name"]
                ]

                widths = [70, 150, 300, 180]

                for value, width in zip(values, widths):

                    ctk.CTkLabel(
                        row,
                        text=value,
                        width=width,
                        anchor="center",
                        font=(settings.FONT, 16),
                        text_color="white"
                    ).pack(side="left")

 
    # --------------------------------------------------

    def back(self):

        self.destroy()

        self.back_callback()