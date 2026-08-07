import json
import os
from datetime import datetime

from data.paths import get_highscore_path

class ScoreManager:

    def __init__(self):

        self.file = get_highscore_path()
        self.score = 0

        self.data = self.load_data()

    # -----------------------------------------

    def load_data(self):

        if not os.path.exists(self.file):

            return {
                "local": [],
                "global": []
            }

        with open(self.file, "r") as f:

            return json.load(f)

    # -----------------------------------------

    def save_data(self):

        with open(self.file, "w") as f:

            json.dump(
                self.data,
                f,
                indent=4
            )

    # -----------------------------------------

    def add(self, points):

        self.score += points

    # -----------------------------------------

    def save_local_score(self, name):

        self.data["local"].append({

            "name": name,

            "score": self.score,

            "time": datetime.now().strftime("%d %b %Y %H:%M")

        })

        self.data["local"].sort(

            key=lambda x: x["score"],

            reverse=True

        )

        self.data["local"] = self.data["local"][:100]

        self.save_data()

    # -----------------------------------------

    def get_local_scores(self):

        return self.data["local"]

    # -----------------------------------------

    def get_best_score(self):

        if len(self.data["local"]) == 0:

            return None

        return self.data["local"][0]
    
    def update_name(self, index, new_name):

        self.data["local"][index]["name"] = new_name

        self.save_data()