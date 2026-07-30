import customtkinter as ctk

import settings
from ui.widgets import GameButton


class SettingsMenu(ctk.CTkFrame):

    def __init__(self, parent, back_callback):

        super().__init__(parent)

        self.configure(
            fg_color=settings.BACKGROUND
        )

        self.pack(fill="both", expand=True)

        self.back_callback = back_callback

        self.build()

    # =====================================================

    def build(self):

        # ---------------- Top Bar ----------------

        top_bar = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=50
        )

        top_bar.pack(fill="x", padx=30, pady=(25,20))
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

        ctk.CTkLabel(
            top_bar,
            text="SETTINGS",
            font=(settings.FONT,48),
            text_color="white"
        ).grid(row=0,column=1)

        ctk.CTkLabel(
            top_bar,
            text="",
            width=170
        ).grid(row=0,column=2)

        # ---------------- Main Box ----------------

        box = ctk.CTkFrame(
            self,
            width=720,
            height=520,
            fg_color="black",
            border_width=3,
            border_color="white",
            corner_radius=0
        )

        box.pack(pady=15)

        box.pack_propagate(False)

        # =====================================================
        # AUDIO
        # =====================================================

        ctk.CTkLabel(
            box,
            text="AUDIO",
            font=(settings.FONT,24),
            text_color="white"
        ).pack(anchor="w", padx=30, pady=(25,15))

        self.sound_slider = self.make_slider(
            box,
            "Sound Effects",
            70
        )

        self.music_slider = self.make_slider(
            box,
            "Music",
            50
        )

        self.separator(box)

        # =====================================================
        # GAMEPLAY
        # =====================================================

        ctk.CTkLabel(
            box,
            text="GAMEPLAY",
            font=(settings.FONT,24),
            text_color="white"
        ).pack(anchor="w", padx=30, pady=(20,15))

        self.mouse_slider = self.make_slider(
            box,
            "Mouse Sensitivity",
            50
        )

        self.separator(box)

        # =====================================================
        # CONTROLS
        # =====================================================

        ctk.CTkLabel(
            box,
            text="CONTROLS",
            font=(settings.FONT,24),
            text_color="white"
        ).pack(anchor="w", padx=30, pady=(20,15))

        self.control_row(box,"Move Left","A")
        self.control_row(box,"Move Right","D")
        self.control_row(box,"Shoot","SPACE")
        self.control_row(box,"Pause","ESC")

        GameButton(
            box,
            text="SAVE",
            width=220,
            command=self.save
        ).pack(pady=30)

    # =====================================================

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