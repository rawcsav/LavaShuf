import os
import tkinter as tk
from tkinter import messagebox
from spotify import SpotifyRandomQueue
from detection import LavaLampRandomGenerator
from dotenv import load_dotenv

load_dotenv()

class LavaLampApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lava Lamp Random Number Generator")
        self.generator = LavaLampRandomGenerator(video_source=0, model_path="../runs/run2/weights/last.pt")
        self.spotify_random_queue = None

        self.setup_ui()

    def setup_ui(self):
        self.start_button = tk.Button(self.root, text="Start", command=self.start)
        self.start_button.pack(pady=20)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.pack(pady=20)

    def start(self):
        if not self.generator.display_only():
            messagebox.showinfo("Info", "User canceled. Exiting.")
            return

        spotify_client_id = os.getenv("CLIENT_ID")
        spotify_client_secret = os.getenv("CLIENT_SECRET")
        spotify_redirect_uri = os.getenv("REDIRECT_URI")
        self.spotify_random_queue = SpotifyRandomQueue(spotify_client_id,
                                                       spotify_client_secret,
                                                       spotify_redirect_uri)

        user_playlists = self.spotify_random_queue.get_user_playlists()
        playlist_names = [playlist['name'] for playlist in user_playlists]

        playlist_index = self.select_playlist(playlist_names)
        if playlist_index is None:
            return

        selected_playlist = user_playlists[playlist_index]
        playlist_id = selected_playlist['id']
        playlist_length = selected_playlist['tracks']['total']

        num_songs = self.get_num_songs()
        if num_songs is None:
            return

        random_indices = self.generate_random_indices(num_songs, playlist_length)
        if not random_indices:
            return

        queued_songs = self.spotify_random_queue.queue_random_songs(playlist_id,
                                                                    random_indices)
        self.display_queued_songs(queued_songs)

    def select_playlist(self, playlist_names):
        playlist_window = tk.Toplevel(self.root)
        playlist_window.title("Select Playlist")

        tk.Label(playlist_window, text="Available playlists:").pack(pady=10)
        playlist_listbox = tk.Listbox(playlist_window)
        for name in playlist_names:
            playlist_listbox.insert(tk.END, name)
        playlist_listbox.pack(pady=10)

        selected_index = []

        def on_select():
            selected_index.append(playlist_listbox.curselection())
            if selected_index[0]:
                playlist_window.destroy()
            else:
                messagebox.showwarning("Warning", "Please select a playlist.")

        select_button = tk.Button(playlist_window, text="Select", command=on_select)
        select_button.pack(pady=10)

        self.root.wait_window(playlist_window)
        return selected_index[0][0] if selected_index else None

    def get_num_songs(self):
        num_songs_window = tk.Toplevel(self.root)
        num_songs_window.title("Number of Songs")

        tk.Label(num_songs_window, text="Enter the number of songs to queue:").pack(pady=10)
        num_songs_entry = tk.Entry(num_songs_window)
        num_songs_entry.pack(pady=10)

        num_songs = []

        def on_submit():
            try:
                num = int(num_songs_entry.get())
                if num <= 0:
                    raise ValueError("Number of songs must be positive.")
                num_songs.append(num)
                num_songs_window.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        submit_button = tk.Button(num_songs_window, text="Submit", command=on_submit)
        submit_button.pack(pady=10)

        self.root.wait_window(num_songs_window)
        return num_songs[0] if num_songs else None

    def generate_random_indices(self, num_songs, playlist_length):
        blob_data_list = []
        random_indices = []

        while len(random_indices) < num_songs:
            blob_data = self.generator.get_blob_data()

            if blob_data:
                blob_data_list.append(blob_data)
                random_index = self.generator.generate_random_number(blob_data, 0,
                                                                     playlist_length - 1)

                if random_index not in random_indices:
                    random_indices.append(random_index)
            else:
                print("No blob data found. Retrying...")

        # Display blob data used for RNG in a pop-up window
        blob_data_info = [
            f"Blob data {i} - Generated random index: {random_index} using: {blob_data}"
            for i, (blob_data, random_index) in
            enumerate(zip(blob_data_list, random_indices), start=1)
        ]
        self.display_info_window("Blob Data Used for RNG", blob_data_info)

        return random_indices

    def display_info_window(self, title, info_list):
        info_window = tk.Toplevel(self.root)
        info_window.title(title)

        window_frame = tk.Frame(info_window)
        window_frame.pack(fill=tk.BOTH, expand=True)

        listbox = tk.Listbox(window_frame, width=50, height=10)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(window_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        for info in info_list:
            listbox.insert(tk.END, info)

    def display_queued_songs(self, queued_songs):
        songs_window = tk.Toplevel(self.root)
        songs_window.title("Queued Songs")

        tk.Label(songs_window, text="Queued Songs:").pack(pady=10)
        for i, song in enumerate(queued_songs, start=1):
            song_info = f"{i}. {song['name']} - {', '.join([artist['name'] for artist in song['artists']])}"
            tk.Label(songs_window, text=song_info).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = LavaLampApp(root)
    root.mainloop()