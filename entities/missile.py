import math
from PIL import Image, ImageTk
import settings


class Missile:

    def __init__(self, canvas, x, y, angle):

        self.canvas = canvas

        self.speed = settings.MISSILE_SPEED

        self.angle = angle

        image = Image.open("assets/images/missile.png")
        image = image.resize(
            (
                settings.MISSILE_WIDTH,
                settings.MISSILE_HEIGHT
            ),
            Image.NEAREST
        )

        # Rotate missile to match ship
        rotated = image.rotate(
            angle,
            resample=Image.NEAREST,
            expand=True
        )

        self.photo = ImageTk.PhotoImage(rotated)

        self.sprite = canvas.create_image(
            x,
            y,
            image=self.photo
        )

        # Direction vector
        radians = math.radians(-angle)

        self.vx = self.speed * math.sin(radians)
        self.vy = -self.speed * math.cos(radians)

    def update(self):

        self.canvas.move(
            self.sprite,
            self.vx,
            self.vy
        )

    def is_offscreen(self):

        x, y = self.canvas.coords(self.sprite)

        return (
            x < -50
            or x > settings.WINDOW_WIDTH + 50
            or y < -50
            or y > settings.WINDOW_HEIGHT + 50
        )

    def destroy(self):

        self.canvas.delete(self.sprite)