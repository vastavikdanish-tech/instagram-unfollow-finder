# =========================================================
# INSTAGRAM UNFOLLOW FINDER PRO
# FINAL ULTRA STABLE VERSION 🔥
# =========================================================
#
# INSTALL:
#
# pip install selenium
# pip install customtkinter
# pip install chromedriver-autoinstaller
#
# RUN:
#
# py gui.py
#
# =========================================================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import chromedriver_autoinstaller
import customtkinter as ctk

import threading
import time

# =========================================================
# APP SETTINGS
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

driver = None

followers = []
following = []
unfollowers = []

# =========================================================
# LOGIN FUNCTION
# =========================================================

def login_instagram():

    global driver

    try:

        status_label.configure(
            text="Opening Instagram...",
            text_color="#00ff99"
        )

        # AUTO INSTALL CORRECT DRIVER
        chromedriver_autoinstaller.install()

        options = Options()

        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("detach", True)

        # IMPORTANT
        driver = webdriver.Chrome(options=options)

        driver.get("https://www.instagram.com")

        status_label.configure(
            text="Login manually then open YOUR profile 😈",
            text_color="#00ff99"
        )

    except Exception as e:

        status_label.configure(
            text="Chrome Error!",
            text_color="red"
        )

        result_box.delete("1.0", "end")
        result_box.insert("end", str(e))


# =========================================================
# GET USERNAME
# =========================================================

def get_username():

    try:

        url = driver.current_url

        if "instagram.com/" in url:

            username = url.split("instagram.com/")[1].split("/")[0]

            return username

        return None

    except:
        return None


# =========================================================
# GET USERS
# =========================================================

def get_users():

    users = set()

    try:

        # WAIT
        time.sleep(4)

        # FIND SCROLL BOX
        dialog = driver.find_element(
            By.XPATH,
            "//div[@role='dialog']//div[contains(@style,'overflow')]"
        )

        last_height = 0
        same_count = 0

        while True:

            links = dialog.find_elements(By.TAG_NAME, "a")

            for link in links:

                try:

                    href = link.get_attribute("href")

                    if href and "instagram.com" in href:

                        username = href.rstrip("/").split("/")[-1]

                        blacklist = [
                            "",
                            "explore",
                            "reels",
                            "stories",
                            "accounts",
                            "developer",
                            "about",
                            "p",
                            "following",
                            "followers",
                            "instagram",
                            "direct",
                            "challenge",
                            "emails",
                            "notifications"
                        ]

                        if username not in blacklist:
                            users.add(username)

                except:
                    pass

            # SCROLL
            driver.execute_script("""
                arguments[0].scrollTop =
                arguments[0].scrollHeight
            """, dialog)

            time.sleep(2)

            # CHECK NEW HEIGHT
            new_height = driver.execute_script("""
                return arguments[0].scrollHeight
            """, dialog)

            if new_height == last_height:
                same_count += 1
            else:
                same_count = 0

            last_height = new_height

            # STOP
            if same_count >= 5:
                break

        return list(users)

    except Exception as e:

        result_box.delete("1.0", "end")
        result_box.insert("end", str(e))

        return []


# =========================================================
# SCAN FUNCTION
# =========================================================

def start_scan():

    threading.Thread(target=scan_account).start()


def scan_account():

    global followers
    global following
    global unfollowers

    try:

        status_label.configure(
            text="Scanning...",
            text_color="#00ff99"
        )

        username = get_username()

        if not username:

            status_label.configure(
                text="Open your Instagram profile first!",
                text_color="red"
            )

            return

        # =================================================
        # FOLLOWERS
        # =================================================

        driver.get(
            f"https://www.instagram.com/{username}/followers/"
        )

        time.sleep(5)

        followers = get_users()

        followers_count.configure(
            text=str(len(followers))
        )

        # =================================================
        # FOLLOWING
        # =================================================

        driver.get(
            f"https://www.instagram.com/{username}/following/"
        )

        time.sleep(5)

        following = get_users()

        following_count.configure(
            text=str(len(following))
        )

        # =================================================
        # FIND UNFOLLOWERS
        # =================================================

        unfollowers = []

        for user in following:

            if user not in followers:
                unfollowers.append(user)

        unfollowers_count.configure(
            text=str(len(unfollowers))
        )

        # =================================================
        # SHOW RESULTS
        # =================================================

        result_box.delete("1.0", "end")

        result_box.insert(
            "end",
            "🔥 UNFOLLOWERS FOUND:\n\n"
        )

        for user in unfollowers:

            result_box.insert(
                "end",
                f"❌ {user}\n"
            )

        if len(unfollowers) == 0:

            result_box.insert(
                "end",
                "😎 No unfollowers found!"
            )

        status_label.configure(
            text="Scan Completed Successfully 😈",
            text_color="#00ff99"
        )

    except Exception as e:

        status_label.configure(
            text="Scan Failed!",
            text_color="red"
        )

        result_box.delete("1.0", "end")
        result_box.insert("end", str(e))


# =========================================================
# UI
# =========================================================

root = ctk.CTk()

root.geometry("1400x850")
root.title("Instagram Unfollow Finder Pro")

# =========================================================
# SIDEBAR
# =========================================================

sidebar = ctk.CTkFrame(
    root,
    width=220,
    corner_radius=0
)

sidebar.pack(side="left", fill="y")

logo = ctk.CTkLabel(
    sidebar,
    text="Insta Pro",
    font=("Arial", 32, "bold")
)

logo.pack(pady=40)

buttons = [
    "Dashboard",
    "Unfollowers",
    "Ghost Followers",
    "Analytics",
    "Export Data",
    "Settings"
]

for btn in buttons:

    ctk.CTkButton(
        sidebar,
        text=btn,
        width=170,
        height=45,
        corner_radius=12
    ).pack(pady=12)

# =========================================================
# MAIN
# =========================================================

main = ctk.CTkFrame(
    root,
    fg_color="transparent"
)

main.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

title = ctk.CTkLabel(
    main,
    text="◎ Instagram Unfollow Finder Pro",
    font=("Arial", 42, "bold")
)

title.pack(pady=(20, 0))

subtitle = ctk.CTkLabel(
    main,
    text="Real Login + Real Scan 😈💧",
    font=("Arial", 22)
)

subtitle.pack(pady=(0, 25))

# =========================================================
# STATUS
# =========================================================

status_label = ctk.CTkLabel(
    main,
    text="READY 🚀",
    font=("Arial", 18, "bold"),
    text_color="#00ff99"
)

status_label.pack(pady=10)

# =========================================================
# BUTTONS
# =========================================================

button_frame = ctk.CTkFrame(
    main,
    fg_color="transparent"
)

button_frame.pack(pady=15)

login_btn = ctk.CTkButton(
    button_frame,
    text="🔐 LOGIN INSTAGRAM",
    width=250,
    height=55,
    font=("Arial", 20, "bold"),
    corner_radius=15,
    fg_color="#00d4ff",
    hover_color="#00aaff",
    command=login_instagram
)

login_btn.grid(row=0, column=0, padx=20)

scan_btn = ctk.CTkButton(
    button_frame,
    text="🚀 START SCAN",
    width=250,
    height=55,
    font=("Arial", 20, "bold"),
    corner_radius=15,
    fg_color="#ff7ad9",
    hover_color="#ff4fc3",
    command=start_scan
)

scan_btn.grid(row=0, column=1, padx=20)

# =========================================================
# STATS
# =========================================================

stats_frame = ctk.CTkFrame(
    main,
    fg_color="transparent"
)

stats_frame.pack(pady=25)

def create_stat(title_text, value):

    frame = ctk.CTkFrame(
        stats_frame,
        width=160,
        height=140,
        corner_radius=20
    )

    frame.pack(side="left", padx=25)

    title = ctk.CTkLabel(
        frame,
        text=title_text,
        font=("Arial", 22)
    )

    title.pack(pady=(22, 10))

    value_label = ctk.CTkLabel(
        frame,
        text=value,
        font=("Arial", 42, "bold"),
        text_color="#ffee58"
    )

    value_label.pack()

    return value_label

followers_count = create_stat("Followers", "0")
following_count = create_stat("Following", "0")
unfollowers_count = create_stat("Unfollowers", "0")

# =========================================================
# SEARCH
# =========================================================

search_box = ctk.CTkEntry(
    main,
    width=850,
    height=55,
    placeholder_text="🔍 Search username...",
    corner_radius=18,
    font=("Arial", 18)
)

search_box.pack(pady=20)

# =========================================================
# RESULT BOX
# =========================================================

result_box = ctk.CTkTextbox(
    main,
    width=950,
    height=320,
    corner_radius=20,
    font=("Consolas", 18)
)

result_box.pack(pady=22)

result_box.insert(
    "end",
    "🔥 READY FOR SCAN..."
)

# =========================================================
# START APP
# =========================================================
credit_label = ctk.CTkLabel(
    root,
    text="Made by Danish 🚀",
    text_color="#888888",
    font=("Arial", 12)
)

credit_label.place(x=20, y=740)
root.mainloop()