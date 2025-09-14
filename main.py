#main.py
from gui import start_app
from music_controller import load_playlist

if __name__ == "__main__":
    load_playlist()  # Initialize the playlist first
    start_app()      # Then start the GUI
