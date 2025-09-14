#music controller
from db_playlist import get_songs, insert_play_history, get_song_id
import pygame #used for playing audio

# Initialize mixer
pygame.mixer.init() #initialize pygame music system before playing any audio

# Fetch songs from the database
global songs, current_index, is_paused, is_playing
songs = get_songs()  # This will return a list of tuples (song_name, song_path)
current_index = 0 #to track current song
is_playing = False #flag if a song is playing or not
is_paused = False #if song is paused or not

def load_playlist():
    #Initialize the playlist from database
    global songs, current_index   #accessing global variables
    songs = get_songs()
    current_index = 0 if songs else -1  #if songs are there start from song 0, if no songs set -1
    print(f"🎵 Loaded {len(songs)} songs from database")

#sets a playlist manually by giving song list
def setPlaylist(new_playlist):
    global songs
    songs = new_playlist

def get_current_song_path():
    #Returns the current song path or None
    if songs and 0 <= current_index < len(songs):
        return songs[current_index][1]  # Return the path part of the tuple
    return None

def playMusic():
    global is_playing, is_paused
    if is_paused:
        return resumeMusic()
    
    song_path = get_current_song_path()
    if not song_path:
        print("⚠️ No song selected!")
        return

    try:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        is_playing = True
        is_paused = False
        print(f"🎶 Now playing: {songs[current_index][0]}")
        if song_id := get_song_id(song_path): #used walrus operator which cheks if song exists and fetches the value
            insert_play_history(song_id)

    except Exception as e:
        print(f"Error: {e}")
      


def pause():
    global is_paused
    if pygame.mixer.music.get_busy():# checks if music is playing or paused
        pygame.mixer.music.pause()
        is_paused = True #accordingly change the value of gloabal variable
    else:
        pygame.mixer.music.unpause()
        is_paused = False  


def resumeMusic():
    global is_paused
    pygame.mixer.music.unpause()
    is_paused = False

def play_next():
    global current_index,is_paused
    if songs:
        current_index = (current_index + 1) % len(songs)
        is_paused = False   # <--- important
        playMusic()
        
        

def play_previous():
    global current_index,is_paused
    if songs:
        current_index = (current_index - 1 + len(songs)) % len(songs)
        is_paused = False   # <--- important
        playMusic()
     
       
