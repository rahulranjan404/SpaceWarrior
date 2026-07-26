from PIL import Image, ImageTk
import settings


class Explosion:

    def __init__(self, canvas, x, y, explosion_type="impact", size=64):

        self.canvas = canvas

        self.type = explosion_type

        self.frame = 0

        self.counter = 0

        self.frame_delay = 3

        self.finished = False

        # ----------------------------------------------------

        sheet = Image.open(
            "assets/images/impact_explosion.png"
        ).convert("RGBA")

        self.frames = []

        FRAME_SIZE = 64

        for i in range(4):

            img = sheet.crop((
                i * FRAME_SIZE,
                0,
                (i + 1) * FRAME_SIZE,
                FRAME_SIZE
            ))

            img = img.resize(
                (size, size),
                Image.NEAREST
            )

            self.frames.append(
                ImageTk.PhotoImage(img)
            )

        # ----------------------------------------------------

        self.sprite = canvas.create_image(
            x,
            y,
            image=self.frames[0]
        )

    # ======================================================

    def update(self):

        self.counter += 1

        if self.counter < self.frame_delay:
            return

        self.counter = 0

        self.frame += 1

        if self.frame >= len(self.frames):

            self.finished = True

            self.canvas.delete(self.sprite)

            return

        self.canvas.itemconfig(
            self.sprite,
            image=self.frames[self.frame]
        )