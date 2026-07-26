import random
from PIL import Image, ImageTk
import settings


class Asteroid:

    def __init__(self, canvas):

        self.canvas = canvas

        # -----------------------------
        # Random properties
        # -----------------------------
        self.knockback_x = 0
        self.knockback_y = 0

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
            self.mass = 1

        elif self.size <= 75:
            self.hp = 2
            self.mass = 2

        else:
            self.hp = 3
            self.mass = 3

    # =====================================

    def update(self):

        self.x += self.vx + self.knockback_x
        self.y += self.vy + self.knockback_y

        self.knockback_x *= 0.85
        self.knockback_y *= 0.85

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

    def apply_knockback(self, dx, dy):

        strength = 2.5 / self.mass
    
        self.knockback_x += dx * strength
        self.knockback_y += dy * strength