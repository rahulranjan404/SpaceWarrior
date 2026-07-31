from email.mime import audio

import customtkinter as ctk
import settings

from ui.menu import MainMenu


class SpaceWarrior(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode(settings.THEME)
        ctk.set_default_color_theme(settings.COLOR_THEME)

        self.title(settings.TITLE)
        self.geometry(
            f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}"
        )

        self.resizable(False, False)

        self.current_screen = None

        self.show_menu()


        from audio import audio

        audio.load(
            "click",
            "assets/sounds/ui.mp3"
        )

        audio.load(
            "explosion",
            "assets/sounds/explosion.mp3"
        )

        audio.load(
            "hover",
            "assets/sounds/hover.mp3"
        )

        audio.load(
            "shoot",
            "assets/sounds/pewpew.mp3"
        )

        audio.load(
            "alive",
            "assets/sounds/bgsoundplayer.mp3"
        )



        # print("Loaded audio files")

    def change_screen(self, screen):

        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = screen(self)
        self.current_screen.pack(fill="both", expand=True)

    def show_menu(self):
        self.change_screen(MainMenu)


if __name__ == "__main__":
    app = SpaceWarrior()
    app.mainloop()