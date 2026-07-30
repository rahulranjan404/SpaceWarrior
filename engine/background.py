import random
import settings

class StarField:

    def __init__(self, canvas, width, height):

        self.canvas = canvas
        self.width = width
        self.height = height

        self.stars = []
        self.speed_multiplier = settings.speed_multiplier

        self.create_layer(70, 1, (1, 2))
        self.create_layer(45, 2, (2, 3))
        self.create_layer(25, 4, (2, 3))

    def create_layer(self, count, speed, size_range):

        for _ in range(count):

            x = random.randint(0, self.width)
            y = random.randint(0, self.height)

            size = random.randint(size_range[0], size_range[1])

            star = self.canvas.create_oval(
                x,
                y,
                x + size,
                y + size,
                fill="white",
                outline=""
            )

            self.stars.append({
                "id": star,
                "speed": speed,
                "size": size
            })

    def update(self):

        for star in self.stars:

            self.canvas.move(
                star["id"],
                0,
                star["speed"] * self.speed_multiplier
            )

            x1, y1, x2, y2 = self.canvas.coords(star["id"])

            if y1 > self.height:

                x = random.randint(0, self.width)

                self.canvas.coords(
                    star["id"],
                    x,
                    -5,
                    x + star["size"],
                    -5 + star["size"]
                )