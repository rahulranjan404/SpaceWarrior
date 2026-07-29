import customtkinter as ctk
import settings
from audio import audio

class GameButton(ctk.CTkButton):

    def __init__(
        self,
        parent,
        text,
        command,
        width=280,
        height=48
    ):

        def wrapped_command():

            audio.play("click")

            if command:
                command()

        super().__init__(
            parent,

            text=text,
            command=wrapped_command,

            width=width,
            height=height,

            corner_radius=0,

            fg_color=settings.BLACK,

            hover_color=settings.WHITE,

            border_width=2,

            border_color=settings.WHITE,

            text_color=settings.WHITE,

            font=(settings.FONT, settings.BUTTON_SIZE),

            cursor="hand2"
        )

        self.bind("<Enter>", self.hover_in)
        self.bind("<Leave>", self.hover_out)

    def hover_in(self, event):
        self.configure(
            fg_color=settings.WHITE,
            text_color=settings.BLACK
        )

    def hover_out(self, event):
        self.configure(
            fg_color=settings.BLACK,
            text_color=settings.WHITE
        )