import threading
import queue
import time
import vlc
import yt_dlp
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn, TimeRemainingColumn # <--- Fixed this
from rich.panel import Panel
from rich.layout import Layout

console = Console()

class UmamusumeAudioEngine:
    def __init__(self):
        self.songs = [
            "Umapyoi Legend うまぴょい伝説 Official",
            "U.M.A. NEW WORLD!! Umamusume Official",
            "BRIGHTEST HEART Oguri Cap Umamusume",
            "NEXT FRONTIER Umamusume Official"
        ]
        self.queue = queue.Queue(maxsize=2)
        # Added a longer network-caching value for smoother playback
        self.vlc_instance = vlc.Instance("--no-video --quiet --network-caching=5000")
        self.player = self.vlc_instance.media_player_new()
        self.current_meta = {"title": "Initializing...", "duration": 0}
        self.is_running = True

    def extract_stream(self, query):
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch1:{query}", download=False)['entries'][0]
                return {
                    'url': info['url'],
                    'title': info['title'],
                    'duration': info.get('duration', 0)
                }
            except Exception:
                return None

    def producer_thread(self):
        for song_query in self.songs:
            if not self.is_running: break
            stream_data = self.extract_stream(song_query)
            if stream_data:
                self.queue.put(stream_data)
        self.queue.put(None) 

    def get_ui_layout(self, progress_bar):
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body", size=10),
            Layout(name="footer", size=3)
        )
        
        table = Table(show_header=True, header_style="bold cyan", expand=True)
        table.add_column("Engine Status", style="dim", width=15)
        table.add_column("Current Live Performance", style="bold magenta")
        
        state = str(self.player.get_state()).split('.')[-1]
        table.add_row(state, self.current_meta['title'])
        
        layout["header"].update(Panel("[bold green]Umamusume: Pretty Derby - G1 HyperStreamer[/bold green]", border_style="green"))
        layout["body"].update(Panel(table, title="Race Log", border_style="magenta"))
        layout["footer"].update(progress_bar)
        return layout

    def start(self):
        threading.Thread(target=self.producer_thread, daemon=True).start()

        progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=None),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(), # Now properly imported!
        )
        task_id = progress.add_task("Waiting for stream...", total=100)

        with Live(self.get_ui_layout(progress), refresh_per_second=4) as live:
            while self.is_running:
                if self.player.get_state() in [vlc.State.Ended, vlc.State.NothingSpecial, vlc.State.Stopped]:
                    next_track = self.queue.get()
                    if next_track is None: break 
                    
                    self.current_meta = next_track
                    media = self.vlc_instance.media_new(next_track['url'])
                    self.player.set_media(media)
                    self.player.play()
                    progress.update(task_id, total=next_track['duration'], completed=0, description="Racing...")

                if self.player.is_playing():
                    cur_time = self.player.get_time() / 1000
                    progress.update(task_id, completed=cur_time)
                
                live.update(self.get_ui_layout(progress))
                time.sleep(0.5)

if __name__ == "__main__":
    engine = UmamusumeAudioEngine()
    try:
        engine.start()
    except KeyboardInterrupt:
        engine.is_running = False
        engine.player.stop()
        console.print("\n[bold red]Race terminated by Trainer.[/bold red]")