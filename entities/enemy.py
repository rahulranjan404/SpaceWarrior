from PIL import Image, ImageTk
import random
import settings


class Enemy:

    SPEED = 4

    def __init__(self, canvas):

        self.canvas = canvas

        self.width = 64
        self.height = 64

        image = Image.open("assets/images/enemy1.png")
        image = image.resize((64, 64), Image.NEAREST)

        self.photo = ImageTk.PhotoImage(image)

        self.x = random.randint(40, settings.WINDOW_WIDTH - 40)
        self.y = -50

        self.sprite = canvas.create_image(
            self.x,
            self.y,
            image=self.photo
        )

    def update(self):

        self.y += self.SPEED

        self.canvas.coords(
            self.sprite,
            self.x,
            self.y
        )

    def offscreen(self):

        return self.y > settings.WINDOW_HEIGHT + 60

    def destroy(self):

        self.canvas.delete(self.sprite)