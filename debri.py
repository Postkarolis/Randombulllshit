import yt_dlp
import vlc
import tkinter as tk
from tkinter import messagebox

# Song metadata and search queries
SONGS = [
    {"title": "Figure.09", "artist": "Linkin Park", "query": "Linkin Park Figure.09 official audio"},
    {"title": "Easier To Run", "artist": "Linkin Park", "query": "Linkin Park Easier To Run official audio"},
    {"title": "Nangs", "artist": "Tame Impala", "query": "Tame Impala Nangs official audio"},
    {"title": "Runaway", "artist": "Linkin Park", "query": "Linkin Park Runaway official audio"},
]

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Ad-Free Stream Player")
        self.root.geometry("400x450")
        
        self.instance = vlc.Instance("--no-video --quiet")
        self.player = self.instance.media_player_new()
        
        self.label = tk.Label(root, text="Select a Song to Stream", font=("Arial", 12, "bold"), pady=20)
        self.label.pack()

        # Create buttons for each song
        for song in SONGS:
            btn_text = f"{song['artist']} - {song['title']}"
            btn = tk.Button(root, text=btn_text, width=40, command=lambda s=song: self.play_song(s))
            btn.pack(pady=5)

        # Control Buttons
        self.stop_btn = tk.Button(root, text="Stop", width=10, bg="#ff4d4d", command=self.stop_audio)
        self.stop_btn.pack(pady=20)

        self.status = tk.Label(root, text="Status: Idle", fg="grey")
        self.status.pack(side="bottom", pady=10)

    def get_stream_url(self, query):
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info:
                return info['entries'][0]['url']
            return info['url']

    def play_song(self, song):
        self.status.config(text=f"Status: Fetching stream...", fg="orange")
        self.root.update_idletasks()
        
        try:
            stream_url = self.get_stream_url(song['query'])
            media = self.instance.media_new(stream_url)
            self.player.set_media(media)
            self.player.play()
            self.status.config(text=f"Status: Playing {song['title']}", fg="green")
        except Exception as e:
            messagebox.showerror("Error", f"Could not play song: {e}")
            self.status.config(text="Status: Error", fg="red")

    def stop_audio(self):
        self.player.stop()
        self.status.config(text="Status: Stopped", fg="grey")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()