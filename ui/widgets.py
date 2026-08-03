import tkinter as tk
import customtkinter as ctk

import settings
from engine.audio import audio


class GameButton(tk.Canvas):

    def __init__(
        self,
        parent,
        text,
        command,
        width=280,
        height=48,
        style="small"
    ):

        # ===================================================
        # CUSTOMIZATION
        # ===================================================

        # Normal button size
        self.button_width = width
        self.button_height = height
        self.normal_font_size = settings.BUTTON_SIZE

        if style == "small":

            # Hover growth
            self.hover_width_increase = 10
            self.hover_height_increase = 4
            self.hover_font_size = settings.BUTTON_SIZE + 1
        # Font sizes
        
        if style == "default":

            # Hover growth
            self.hover_width_increase = 30
            self.hover_height_increase = 12
            self.hover_font_size = settings.BUTTON_SIZE + 5
        

        # Border thickness
        self.normal_border = 2
        self.hover_border = 2

        # Colours
        self.normal_bg = settings.BLACK
        self.normal_text = settings.WHITE
        self.normal_border_color = settings.WHITE

        self.hover_bg = settings.WHITE
        self.hover_text = settings.BLACK
        self.hover_border_color = settings.BLACK

        # ===================================================

        self.normal_w = self.button_width
        self.normal_h = self.button_height

        self.hover_w = self.button_width + self.hover_width_increase
        self.hover_h = self.button_height + self.hover_height_increase




        super().__init__(

            parent,

            width=self.hover_w,
            height=self.hover_h,

            bg=settings.BACKGROUND,
            highlightthickness=0,
            bd=0,
            cursor="hand2"
        )

        self.command = command
        self.hovered = False
        self.text = text

        self.draw_button(False)

        self.bind("<Enter>", self.hover_in)
        self.bind("<Leave>", self.hover_out)
        self.bind("<Button-1>", self.click)

    # ========================================
    def draw_button(self, hover):

        self.delete("all")

        if hover:

            x = (self.hover_w - self.hover_w) // 2
            y = (self.hover_h - self.hover_h) // 2

            w = self.hover_w
            h = self.hover_h

            fill = self.hover_bg
            outline = self.hover_border_color
            text = self.hover_text
            border = self.hover_border
            font_size = self.hover_font_size

        else:

            x = (self.hover_w - self.normal_w) // 2
            y = (self.hover_h - self.normal_h) // 2

            w = self.normal_w
            h = self.normal_h

            fill = self.normal_bg
            outline = self.normal_border_color
            text = self.normal_text
            border = self.normal_border
            font_size = self.normal_font_size

        self.create_rectangle(
            x,
            y,
            x + w,
            y + h,
            fill=fill,
            outline=outline,
            width=border
        )

        self.create_text(
            self.hover_w // 2,
            self.hover_h // 2,
            text=self.text,
            fill=text,
            font=(settings.FONT, font_size)
        )
    # ========================================

    @property
    def text(self):

        return getattr(self, "_text", "")

    @text.setter
    def text(self, value):

        self._text = value

    # ========================================

    def hover_in(self, event):

        if self.hovered:
            return

        self.hovered = True

        audio.play("hover")

        self.draw_button(True)

    # ========================================

    def hover_out(self, event):

        self.hovered = False

        self.draw_button(False)

    # ========================================

    def click(self, event):

        audio.play("click")

        if self.command:
            self.command()

    # ========================================

    def configure(self, **kwargs):

        if "text" in kwargs:

            self.text = kwargs.pop("text")

            self.draw_button(self.hovered)

        super().configure(**kwargs)