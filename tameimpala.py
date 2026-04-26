import asyncio
import vlc
import yt_dlp
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn
from rich.panel import Panel
from threading import Thread
import time

console = Console()

class TameImpalaPlayer:
    def __init__(self):
        self.instance = vlc.Instance('--no-video --quiet')
        self.player = self.instance.media_player_new()
        self.songs = [
            "The Less I Know The Better",
            "Let It Happen",
            "Feels Like We Only Go Backwards",
            "Borderline"
        ]
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
        }

    def get_stream_url(self, song_name):
        """Extracts the direct audio stream URL to bypass ads."""
        search_query = f"ytsearch1:Tame Impala - {song_name} Official Audio"
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=False)['entries'][0]
            return info['url'], info['title'], info['duration']

    def play_song(self, url):
        media = self.instance.media_new(url)
        self.player.set_media(media)
        self.player.play()

    async def run_playlist(self):
        console.print(Panel("[bold magenta]Tame Impala Ultra-Streamer[/bold magenta]\n[dim]Direct Stream Extraction - No Ads - 4 Iconic Tracks[/dim]", expand=False))
        
        for song in self.songs:
            with console.status(f"[bold cyan]Scraping stream for '{song}'...", spinner="dots"):
                stream_url, title, duration = self.get_stream_url(song)

            self.play_song(stream_url)
            
            console.print(f"\n[bold green]Now Playing:[/bold green] {title}")
            
            # Progress bar simulation synced with VLC duration
            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=console
            ) as progress:
                task = progress.add_task("[magenta]Vibe check in progress...", total=duration)
                
                while self.player.get_state() != vlc.State.Ended:
                    # VLC state 3 is 'Playing', state 6 is 'Ended'
                    if self.player.get_state() == vlc.State.Error:
                        console.print("[bold red]Error: Stream interrupted.[/bold red]")
                        break
                    
                    current_time = self.player.get_time() / 1000  # ms to s
                    progress.update(task, completed=current_time)
                    await asyncio.sleep(1)

        console.print("[bold yellow]Playlist complete. The psychedelic journey ends here.[/bold yellow]")

if __name__ == "__main__":
    player = TameImpalaPlayer()
    try:
        asyncio.run(player.run_playlist())
    except KeyboardInterrupt:
        player.player.stop()
        console.print("\n[bold red]Stream aborted by user.[/bold red]")