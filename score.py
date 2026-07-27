import json
import os


class ScoreManager:

    def __init__(self):

        self.score = 0
        self.file = "highscores.json"

        self.highscore = self.load_highscore()

    def add(self, points):
        self.score += points

    def load_highscore(self):

        if not os.path.exists(self.file):
            return 0

        try:
            with open(self.file, "r") as f:
                data = json.load(f)
                return data.get("highscore", 0)

        except:
            return 0

    def save_highscore(self):

        if self.score > self.highscore:

            self.highscore = self.score

            with open(self.file, "w") as f:
                json.dump(
                    {
                        "highscore": self.highscore
                    },
                    f,
                    indent=4
                )