import pywhatkit
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# -----------------------------------
# CONTACTS
# -----------------------------------

contacts = [
    "+916305519180",
    "+916281363667"
]

# -----------------------------------
# IMAGE PATH
# -----------------------------------

image_path = r"images\cric.jpg"

# -----------------------------------
# CAPTION
# -----------------------------------

caption = """
🏏🔥 CRICKET TOURNAMENT IS HERE! 🔥🏏

Get ready for thrilling matches, explosive sixes, unforgettable wickets, and crowd-roaring moments 🚀

✨ Match Highlights:
🏆 Competitive Teams
🔥 Intense Rivalries
🎯 Big Hits & Wickets
📣 Crowd Energy
💥 Non-stop Entertainment

📢 Gather your squad and witness the action LIVE!

🎟️ Don’t miss the biggest cricket event of the season!
"""

# -----------------------------------
# CHROME DRIVER
# -----------------------------------

service = Service(ChromeDriverManager().install())

options = webdriver.ChromeOptions()

options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=service, options=options)

wait = WebDriverWait(driver, 60)

# -----------------------------------
# LOOP CONTACTS
# -----------------------------------

for number in contacts:

    try:

        print(f"\nSending to {number}")

        # -----------------------------------
        # OPEN IMAGE + CAPTION
        # -----------------------------------

        pywhatkit.sendwhats_image(
            receiver=number,
            img_path=image_path,
            caption=caption,
            wait_time=25,
            tab_close=False,
            close_time=5
        )

        print("Waiting for WhatsApp preview...")

        time.sleep(15)

        # -----------------------------------
        # PRESS SEND BUTTON
        # -----------------------------------

        send_btn = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//span[@data-icon="send"]'
                )
            )
        )

        send_btn.click()

        print(f"✅ Successfully sent to {number}")

        # WAIT BEFORE NEXT CONTACT
        time.sleep(20)

    except Exception as e:

        print(f"❌ Failed for {number}")

        print(e)

print("\n✅ ALL IMAGES SENT SUCCESSFULLY!")

input("Press Enter to close browser...")