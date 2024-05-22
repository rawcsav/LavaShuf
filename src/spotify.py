from spotipy import SpotifyOAuth
import spotipy

class SpotifyRandomQueue:
    def __init__(self, spotify_client_id, spotify_client_secret, spotify_redirect_uri):
        self.spotify_client_id = spotify_client_id
        self.spotify_client_secret = spotify_client_secret
        self.spotify_redirect_uri = spotify_redirect_uri
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.spotify_client_id,
                                                            client_secret=self.spotify_client_secret,
                                                            redirect_uri=self.spotify_redirect_uri,
                                                            scope="playlist-read-private user-modify-playback-state"))

    def get_user_playlists(self):
        playlists = self.sp.current_user_playlists()['items']
        return playlists

    def get_playlist_tracks(self, playlist_id):
        playlist_tracks = self.sp.playlist_items(playlist_id, additional_types=['track'])
        tracks = playlist_tracks['items']
        while playlist_tracks['next']:
            playlist_tracks = self.sp.next(playlist_tracks)
            tracks.extend(playlist_tracks['items'])
        return [track['track'] for track in tracks if 'track' in track]

    def queue_random_songs(self, playlist_id, random_indices):
        playlist_tracks = self.get_playlist_tracks(playlist_id)
        queued_songs = [playlist_tracks[index] for index in random_indices if index < len(playlist_tracks)]
        song_uris = [song['id'] for song in queued_songs]
        for uri in song_uris:
            self.sp.add_to_queue(uri)
        return queued_songs