import os
import sys
import time
import random
import requests
import string
from io import BytesIO


class UsernameRemover:
    def __init__(self):
        self.total_changes = 150

    def print_banner(self):
        print(r"""
====================================================
      FORMER USERNAME REMOVER
               by w4simz
====================================================
        """)

    def generate_random_csrf(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    def display_header(self):
        self.print_banner()
        print("Requirements:")
        print("  • Remove your current profile picture first")
        print("  • Process takes ~25 minutes")
        print("  • Do NOT interrupt")
        print()

    def download_image(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            img_bytes = BytesIO(response.content)
            return {
                "profile_pic": ("profile.jpg", img_bytes, "image/jpeg")
            }
        except Exception:
            return None

    def change_profile_picture(self, sessionid, url_img):
        url = "https://www.instagram.com/accounts/web_change_profile_picture/"
        csrf = self.generate_random_csrf()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/edit/",
            "X-CSRFToken": csrf,
            "Cookie": f"sessionid={sessionid}; csrftoken={csrf};"
        }

        try:
            files = self.download_image(url_img)
            if not files:
                return False

            r = requests.post(url, headers=headers, files=files)
            if r.status_code == 200:
                try:
                    return r.json().get("status") == "ok"
                except:
                    return True
            return False

        except Exception:
            return False

    def login_user(self):
        self.display_header()
        sessionid = input("Enter your Instagram sessionid: ").strip()

        if not sessionid:
            print("\n[ERROR] sessionid cannot be empty.")
            return None

        try:
            url = "https://www.instagram.com/accounts/edit/"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Cookie": f"sessionid={sessionid}"
            }

            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                import re
                match = re.search(r'"username":"([^"]+)"', r.text)
                if match:
                    print(f"\n[OK] Logged in as: @{match.group(1)}")
                else:
                    print("\n[OK] Login successful.")
                time.sleep(1)
                return sessionid
            else:
                print("\n[ERROR] Invalid sessionid.")
                return None

        except Exception:
            print("\n[ERROR] Login failed due to network error.")
            return None

    def change_profile_pictures(self, sessionid):
        pfp_urls = [
            'https://i.ibb.co/pvfHbkTJ/w4simz-1.jpg',
            'https://i.ibb.co/VW0tSZK9/w4simz-2.jpg',
            'https://i.ibb.co/k6QVHvV2/w4simz-3.jpg',
            'https://i.ibb.co/XfvMtDDS/w4simz-4.jpg'
        ]

        change = 0
        errors = 0

        self.print_banner()
        print(f"Target Changes: {self.total_changes}")
        print(f"Using {len(pfp_urls)} rotating images\n")

        while change < self.total_changes:
            for url in pfp_urls:
                if change >= self.total_changes:
                    break

                success = self.change_profile_picture(sessionid, url)

                if success:
                    change += 1
                else:
                    errors += 1

                # Progress bar
                progress = change / self.total_changes
                bar_length = 40
                filled = int(progress * bar_length)
                bar = "█" * filled + "░" * (bar_length - filled)
                percent = int(progress * 100)

                sys.stdout.write(
                    f"\r[{bar}] {percent}% | Changes: {change}/{self.total_changes} | Errors: {errors}"
                )
                sys.stdout.flush()

                time.sleep(10)

        print("\n\nProcess Completed Successfully!")

    def main_removing(self):
        sessionid = self.login_user()
        if sessionid:
            self.change_profile_pictures(sessionid)
        else:
            print("\nExiting.")


def main():
    tool = UsernameRemover()
    tool.main_removing()


if __name__ == "__main__":
    main()
