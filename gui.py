#gui.py

import tkinter as tk
import music_controller  
import threading # Allows running gesture control in background (allows running 2 things at same time (mulitithreading))
import matplotlib.pyplot as plt
from PIL import Image, ImageTk  # 🆕 Added for background image support

# Global variables for UI elements
root = None #main window
song_label = None #will show current song name
btn_pause = None #pause/resume button
play_counts={} # dictionary to track song plays

def update_song_label():
    #Update the song name label
    if music_controller.songs and 0 <= music_controller.current_index < len(music_controller.songs):
        song_name = music_controller.songs[music_controller.current_index][0]  # Get the name part of the tuple
        song_label.config(text=song_name)
    else:
        song_label.config(text="No Song Playing")

def update_pause_button():
    #Update pause button icon
    if btn_pause:
        btn_pause.config(text="⏸️" if not music_controller.is_paused else "▶️")

def force_update_ui():
    """Update all UI elements"""
    update_song_label()
    update_pause_button()

def update_play_count():
    """Fixed version that properly accesses the songs list"""
    if music_controller.songs and 0 <= music_controller.current_index < len(music_controller.songs):
        song_name = music_controller.songs[music_controller.current_index][0]
        play_counts[song_name] = play_counts.get(song_name, 0) + 1

def play_current_song():
    music_controller.playMusic()
    update_play_count()
    force_update_ui()

def toggle_pause_resume():
    music_controller.pause()
    force_update_ui()

def next_song():
    music_controller.play_next()
    update_play_count()
    force_update_ui()

def prev_song():
    music_controller.play_previous()
    update_play_count()
    force_update_ui()

def pause_or_resume():
    toggle_pause_resume()
    force_update_ui()

def start_gesture_control():
    #Runs gesture control in a separate thread
    def run_gesture():
        import gesture_control
        gesture_control.GestureController().run()
    
    gesture_thread = threading.Thread(target=run_gesture, daemon=True) #Start new thread (parallel running) for gesture control so that music player doesn't freeze
    gesture_thread.start()

def show_play_statistics():
    if not play_counts:
        print("No songs played yet!")
        return

    # Filter and sort songs by play count (descending)
    filtered_data = {k: v for k, v in sorted(play_counts.items(),
                                             key=lambda item: item[1], reverse=True) if v > 0}

    if not filtered_data:
        print("No songs have been played yet!")
        return

    songs = list(filtered_data.keys())
    counts = list(filtered_data.values())

    # Create figure with dark theme
    plt.figure(figsize=(10, 8), facecolor='#121212')
    ax = plt.gca()
    ax.set_facecolor('#1E1E1E')

    # Create pie chart with improved settings
    wedges, texts, autotexts = plt.pie(
        counts,
        labels=songs,
        autopct=lambda p: f'{p:.1f}% ({int(p / 100 * sum(counts))} plays)',
        startangle=90,
        colors=plt.cm.tab20.colors,
        textprops={'color': 'white', 'fontsize': 10},
        wedgeprops={'linewidth': 1, 'edgecolor': '#121212'}
    )

    # Style adjustments
    plt.setp(autotexts, size=10, weight="bold")
    plt.title(f'Song Play Statistics\nTotal Plays: {sum(counts)}',
              color='white', fontsize=14, pad=20)

    # Add interactive legend
    legend = plt.legend(
        wedges,
        [f"{song}: {count} plays" for song, count in zip(songs, counts)],
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        facecolor='#1E1E1E',
        edgecolor='white',
        fontsize=10,
        labelcolor='white'
    )

    plt.tight_layout()
    plt.show()

def start_app():
    global root, song_label, btn_pause
    root = tk.Tk()
    root.title("🎵 Music Player")
    root.geometry("800x600")

    # ✅ Load background image AFTER initializing root
    # image = Image.open("C:\Users\Prafulla wate\Desktop\PYTHON\music_player\assets\SL.123119.26540.04.jpg")
    image = Image.open(r"C:\Users\Prafulla wate\Desktop\PYTHON\music_player\assets\SL.123119.26540.04.jpg")
    image = image.resize((800, 600))  # Resize to fit window
    bg_photo = ImageTk.PhotoImage(image)

    # ✅ Create label with image and place it behind everything
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference!
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    # # Initialize window
    # root = tk.Tk() #create the main window
    # root.title("🎵 Music Player")
    # root.geometry("800x600")
    # root.configure(bg="#121212") #dark grey
    
    # Song display
    song_label = tk.Label(root, text="No Song Playing", 
                         font=("Arial", 24), fg="white", bg="#081C26")
    song_label.pack(pady=50)

    # Control buttons
    controls_frame = tk.Frame(root, bg="#081C26")
    controls_frame.pack() #keep all control buttons together

    #creating 4 buttons inside frame
    # Previous button
    btn_prev = tk.Button(controls_frame, text="⏮", font=("Arial", 30), 
                        fg="white", bg="#1DB954", bd=0,
                        command=prev_song)

    # Play button
    btn_play = tk.Button(controls_frame, text="▶", font=("Arial", 30),
                        fg="white", bg="#1DB954", bd=0,
                        command=play_current_song)

    # Pause/Resume button
    btn_pause = tk.Button(controls_frame, text="⏸️", font=("Arial", 30),
                         fg="white", bg="#1DB954", bd=0,
                         command=pause_or_resume)

    # Next button
    btn_next = tk.Button(controls_frame, text="⏭", font=("Arial", 30),
                        fg="white", bg="#1DB954", bd=0,
                        command=next_song)

    # Layout buttons
    btn_prev.grid(row=0, column=0, padx=20)
    btn_play.grid(row=0, column=1, padx=20)
    btn_pause.grid(row=0, column=2, padx=20)
    btn_next.grid(row=0, column=3, padx=20)

    # Gesture control button
    btn_gesture = tk.Button(controls_frame, text="👆 Gesture Control",
                           font=("Arial", 14), fg="white", bg="#1DB954",
                           command=start_gesture_control)
    btn_gesture.grid(row=1, columnspan=4, pady=20)

 # Additional buttons
    btn_stats = tk.Button(controls_frame, text="📈 Show Stats",
                          font=("Arial", 14), fg="white", bg="#1DB954",
                          command=show_play_statistics)
    btn_stats.grid(row=2, columnspan=4, pady=20)

    # Status bar
    status_label = tk.Label(root, text=f"🎵 {len(music_controller.songs)} songs loaded",
                           font=("Arial", 12), fg="grey", bg="#121212")
    status_label.pack(side="bottom", pady=10)
    
    def update_ui():
        update_song_label()
        update_pause_button()
        root.after(100, update_ui)  # Updates every 100ms

    update_ui()  # Start the auto-update loop
    # play_current_song()  # <- Added this to directly play song when you run 
    root.mainloop() #This keeps the window open forever until you close it manually

if __name__ == "__main__":
    start_app()
