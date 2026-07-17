import customtkinter as ctk
import settings

from ui.widgets import GameButton


class PauseMenu(ctk.CTkFrame):

    def __init__(self, parent, continue_callback, menu_callback):
        super().__init__(parent)

        self.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.configure(
            width=350,
            height=260,
            fg_color=settings.BLACK,
            border_width=2,
            border_color=settings.WHITE,
            corner_radius=0
        )

        self.pack_propagate(False)

        title = ctk.CTkLabel(
            self,
            text="PAUSED",
            font=(settings.FONT, 28),
            text_color=settings.WHITE
        )

        title.pack(pady=(25, 20))

        GameButton(
            self,
            "CONTINUE",
            continue_callback,
            width=220
        ).pack(pady=10)

        GameButton(
            self,
            "MAIN MENU",
            menu_callback,
            width=220
        ).pack(pady=10)