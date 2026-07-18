from PIL import Image, ImageTk
import settings
import math


class Player:

    def __init__(self, canvas):

        self.canvas = canvas

        self.width = settings.PLAYER_WIDTH
        self.height = settings.PLAYER_HEIGHT

        self.radius = self.width * 0.30

        self.x = settings.WINDOW_WIDTH // 2
        self.y = settings.WINDOW_HEIGHT - 120

        # Velocity
        self.vx = 0.0
        self.vy = 0.0

        # Controls
        self.left = False
        self.right = False
        self.up = False
        self.down = False

        self.original_image = Image.open(
            "assets/images/spaceship.png"
        ).resize(
            (self.width, self.height),
            Image.NEAREST
        )

        self.angle = 0

        self.photo = ImageTk.PhotoImage(self.original_image)

        self.sprite = self.canvas.create_image(
            self.x,
            self.y,
            image=self.photo
        )

    def update_rotation(self):

        target_angle = 0

        if self.left:
            target_angle = settings.PLAYER_MAX_TILT

        elif self.right:
            target_angle = -settings.PLAYER_MAX_TILT

        if self.angle < target_angle:
            self.angle += settings.PLAYER_TILT_SPEED

        elif self.angle > target_angle:
            self.angle -= settings.PLAYER_TILT_SPEED

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

    def update(self):

        # -----------------------
        # Horizontal
        # -----------------------

        if self.left:
            self.vx -= settings.PLAYER_ACCELERATION

        if self.right:
            self.vx += settings.PLAYER_ACCELERATION

        # -----------------------
        # Vertical
        # -----------------------

        if self.up:
            self.vy -= settings.PLAYER_ACCELERATION

        if self.down:
            self.vy += settings.PLAYER_ACCELERATION

        # -----------------------
        # Friction
        # -----------------------

        if not self.left and not self.right:

            if self.vx > 0:
                self.vx -= settings.PLAYER_FRICTION
                if self.vx < 0:
                    self.vx = 0

            elif self.vx < 0:
                self.vx += settings.PLAYER_FRICTION
                if self.vx > 0:
                    self.vx = 0

        if not self.up and not self.down:

            if self.vy > 0:
                self.vy -= settings.PLAYER_FRICTION
                if self.vy < 0:
                    self.vy = 0

            elif self.vy < 0:
                self.vy += settings.PLAYER_FRICTION
                if self.vy > 0:
                    self.vy = 0

        # -----------------------
        # Clamp speed
        # -----------------------

        self.vx = max(
            -settings.PLAYER_MAX_SPEED,
            min(settings.PLAYER_MAX_SPEED, self.vx)
        )

        self.vy = max(
            -settings.PLAYER_MAX_SPEED,
            min(settings.PLAYER_MAX_SPEED, self.vy)
        )

        # -----------------------
        # Apply movement
        # -----------------------

        self.x += self.vx
        self.y += self.vy

        # -----------------------
        # Keep inside screen
        # -----------------------

        half_w = self.width // 2
        half_h = self.height // 2

        self.x = max(
            half_w,
            min(settings.WINDOW_WIDTH - half_w, self.x)
        )

        self.y = max(
            half_h,
            min(settings.WINDOW_HEIGHT - 60 - half_h, self.y)
        )

        # Stop at borders
        if self.x == half_w or self.x == settings.WINDOW_WIDTH - half_w:
            self.vx = 0

        if self.y == half_h or self.y == settings.WINDOW_HEIGHT - 60 - half_h:
            self.vy = 0

        self.update_rotation()  

        self.canvas.coords(
            self.sprite,
            self.x,
            self.y
        )



    def get_gun_position(self):

        # Use the same angle convention as the missile
        radians = math.radians(-self.angle)

        # Distance from the center of the ship to the nose
        nose_distance = self.height * 0.48

        x = self.x + math.sin(radians) * nose_distance
        y = self.y - math.cos(radians) * nose_distance

        return x, y