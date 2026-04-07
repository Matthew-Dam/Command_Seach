import webbrowser

class MusicSite:
    def __init__(self):
        self.MUSIC_URLS = {
            "Spotify": "https://open.spotify.com",
            "Apple Music": "https://music.apple.com",
            "YouTube Music": "https://music.youtube.com",
            "SoundCloud": "https://soundcloud.com",
            "Deezer": "https://www.deezer.com",
            "Tidal": "https://tidal.com",
            "Pandora": "https://www.pandora.com",
            "Amazon Music": "https://music.amazon.com",
            "Audiomack": "https://audiomack.com",
            "Bandcamp": "https://bandcamp.com",
            "Napster": "https://app.napster.com",
            "Boomplay": "https://www.boomplay.com",
            "Gaana": "https://gaana.com",
            "JioSaavn": "https://www.jiosaavn.com",
            "Anghami": "https://www.anghami.com",
            "Mixcloud": "https://www.mixcloud.com"
        }

    @staticmethod
    def music_smart_search(url, query):
        if "youtube" in url:
            return f"{url}/results?search_query={query}"
        else:
            return f"{url}/search?q={query}"

    @staticmethod
    def webgo(url):
        # edge_path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s"
        webbrowser.open(url)

    def operate_music_site(self, url):
        print(f"Opening {url}...")
        self.webgo(f"{url}")
        searched = False
        while True:
            play = input("Enter a music/artist to listen: ").lower()
            if play == "close":
                webbrowser.open("https://www.bing.com")
                return searched
            search_url = self.music_smart_search(url, play)
            self.webgo(search_url)
            searched = True
