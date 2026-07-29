import customtkinter as ctk
import settings

from ui.widgets import GameButton


class GameOverMenu(ctk.CTkFrame):

    

    def __init__(
        self,
        parent,
        restart_callback,
        exit_callback,
        score,
        highscore
    ):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        #Full-screen overlay
        self.place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )

        # Center panel
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
            command=restart_callback,
            width=220,
            height=45
        ).pack(pady=10)

        GameButton(
            panel,
            text="EXIT",
            command=exit_callback,
            width=220,
            height=45
        ).pack(pady=10)