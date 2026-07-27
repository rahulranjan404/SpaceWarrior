import json
import os
from datetime import datetime


class ScoreManager:

    def __init__(self):

        self.score = 0

        self.file = "highscores.json"

        self.data = self.load_data()

    # -----------------------------

    def load_data(self):

        if not os.path.exists(self.file):

            return {
                "local": {
                    "name": "No Player",
                    "score": 0,
                    "time": "-"
                },
                "global": []
            }

        with open(self.file, "r") as f:

            return json.load(f)

    # -----------------------------

    def save_data(self):

        with open(self.file, "w") as f:

            json.dump(self.data, f, indent=4)

    # -----------------------------

    def add(self, points):

        self.score += points

    # -----------------------------

    def save_local_highscore(self, player_name):

        if self.score <= self.data["local"]["score"]:
            return

        self.data["local"] = {

            "name": player_name,

            "score": self.score,

            "time": datetime.now().strftime("%d %b %Y %H:%M")

        }

        self.save_data()

    # -----------------------------

    def get_local(self):

        return self.data["local"]