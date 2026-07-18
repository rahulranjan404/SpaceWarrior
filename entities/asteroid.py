import random
from PIL import Image, ImageTk
import settings


class Asteroid:

    def __init__(self, canvas):

        self.canvas = canvas

        # -----------------------------
        # Random properties
        # -----------------------------

        self.size = random.randint(
            settings.ASTEROID_MIN_SIZE,
            settings.ASTEROID_MAX_SIZE
        )

        self.radius = self.size * 0.4

        self.x = random.randint(
            self.size,
            settings.WINDOW_WIDTH - self.size
        )

        self.y = -self.size

        self.vx = random.uniform(
            -settings.ASTEROID_MAX_DRIFT,
            settings.ASTEROID_MAX_DRIFT
        )

        self.vy = random.uniform(
            settings.ASTEROID_MIN_SPEED,
            settings.ASTEROID_MAX_SPEED
        )

        self.angle = random.randint(0, 359)

        self.rotation_speed = random.uniform(
            -settings.ASTEROID_MAX_ROTATION_SPEED,
            settings.ASTEROID_MAX_ROTATION_SPEED
        )

        # -----------------------------
        # Load random asteroid image
        # -----------------------------

        image_path = random.choice(settings.ASTEROID_IMAGES)

        self.original_image = Image.open(image_path).resize(
            (self.size, self.size),
            Image.NEAREST
        )

        self.photo = ImageTk.PhotoImage(self.original_image)

        self.sprite = self.canvas.create_image(
            self.x,
            self.y,
            image=self.photo
        )

        if self.size <= 60:
            self.hp = 1

        elif self.size <= 75:
            self.hp = 2

        else:
            self.hp = 3

    # =====================================

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.angle += self.rotation_speed

        rotated = self.original_image.rotate(
            self.angle,
            resample=Image.NEAREST,
            expand=True
        )

        self.photo = ImageTk.PhotoImage(rotated)

        self.canvas.itemconfig(
            self.sprite,
            image=self.photo
        )

        self.canvas.coords(
            self.sprite,
            self.x,
            self.y
        )

    # =====================================

    def is_offscreen(self):

        return (
            self.y > settings.WINDOW_HEIGHT + self.size
        )

    # =====================================
    def take_damage(self):

        self.hp -= 1

        return self.hp <= 0

    def destroy(self):

        self.canvas.delete(self.sprite)