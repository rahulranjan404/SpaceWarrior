import os
import sys


APP_NAME = "SpaceWarrior"


def get_data_directory():

    if sys.platform == "win32":
        # Windows
        base_path = os.getenv("APPDATA")

        if not base_path:
            base_path = os.path.expanduser("~")

        data_dir = os.path.join(
            base_path,
            APP_NAME
        )

    elif sys.platform == "darwin":
        # macOS
        data_dir = os.path.expanduser(
            f"~/Library/Application Support/{APP_NAME}"
        )

    else:
        # Linux
        data_dir = os.path.expanduser(
            f"~/.local/share/{APP_NAME}"
        )

    os.makedirs(data_dir, exist_ok=True)

    return data_dir


def get_settings_path():

    return os.path.join(
        get_data_directory(),
        "settings.json"
    )


def get_highscore_path():

    return os.path.join(
        get_data_directory(),
        "highscores.json"
    )