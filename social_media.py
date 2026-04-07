from movie_sites import *
import webbrowser
class SocialMedia(MovieSites):
    def __init__(self):

        super().__init__()
        self.SOCIAL_LOGIN_URLS = {
            "facebook": "https://www.facebook.com/login",
            "twitter": "https://twitter.com/login",  # now X
            "instagram": "https://www.instagram.com/accounts/login",
            "tiktok": "https://www.tiktok.com/login",
            "snapchat": "https://accounts.snapchat.com/accounts/login",
            "linkedin": "https://www.linkedin.com/login",
            "reddit": "https://www.reddit.com/login",
            "pinterest": "https://www.pinterest.com/login",
            "tumblr": "https://www.tumblr.com/login",
            "threads": "https://www.threads.net/login",
            "whatsapp": "https://web.whatsapp.com",  # login via QR code
            "messenger": "https://www.messenger.com/login",
            "telegram": "https://web.telegram.org",  # login inside web app
            "discord": "https://discord.com/login",
            "wechat": "https://web.wechat.com",  # QR login
            "line": "https://access.line.me/login",
            "vk": "https://vk.com/login"
        }


    def login(self,platform):
        platform = platform.lower()
        url = self.SOCIAL_LOGIN_URLS.get(platform)

        if not url:
            print(f"No login found for {platform}.")
            return False
        print(f"Opening {platform} login...")
        webbrowser.open(url)
        while True:
            choice = input("Social media ground: ").lower()
            if choice == "close":
                webbrowser.open("https://www.bing.com")
                break
        return True
