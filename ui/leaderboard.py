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

        self.build()

    def build(self):

        title = ctk.CTkLabel(
            self,
            text="LEADERBOARD",
            font=(settings.FONT, 36),
            text_color="white"
        )

        title.pack(pady=(30,20))

        tab_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        tab_frame.pack()

        local_btn = GameButton(
            tab_frame,
            text="LOCAL",
            width=160,
            command=lambda: None
        )

        local_btn.pack(side="left", padx=10)

        global_btn = GameButton(
            tab_frame,
            text="GLOBAL",
            width=160,
            command=lambda: None
        )

        global_btn.pack(side="left", padx=10)

        local = self.score_manager.get_local()

        card = ctk.CTkFrame(

            self,

            fg_color="black",

            border_color="white",

            border_width=3,

            corner_radius=0,

            width=700,

            height=240

        )

        card.pack(pady=35)

        card.pack_propagate(False)

        ctk.CTkLabel(

            card,

            text="#1",

            font=(settings.FONT,40),

            text_color="white"

        ).pack(pady=(25,10))

        ctk.CTkLabel(

            card,

            text=f"SCORE : {local['score']}",

            font=(settings.FONT,28),

            text_color="white"

        ).pack()

        ctk.CTkLabel(

            card,

            text=local["name"],

            font=(settings.FONT,24),

            text_color="white"

        ).pack(pady=10)

        ctk.CTkLabel(

            card,

            text=local["time"],

            font=(settings.FONT,18),

            text_color="white"

        ).pack()

        GameButton(

            self,

            text="BACK",

            width=220,

            command=self.back

        ).pack(pady=40)

    def back(self):

        self.destroy()

        self.back_callback()