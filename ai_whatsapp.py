from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse
import time

# -----------------------------------
# CONTACTS
# -----------------------------------

contacts = [
    "916305519180",
    "916281363667"
]

# -----------------------------------
# USER INPUT
# -----------------------------------

topic = input("Enter topic: ")

topic_lower = topic.lower()

# -----------------------------------
# SMART AI MESSAGE
# -----------------------------------

if "music" in topic_lower or "concert" in topic_lower:

    message = f"""
🎵 {topic} is going to be LEGENDARY! 🔥

Feel the beats, enjoy the vibes, and experience an unforgettable night 🎤✨

📢 Bring your friends and join the celebration!
"""

elif "boxing" in topic_lower or "fight" in topic_lower:

    message = f"""
🥊 {topic} is HERE! 🔥

Get ready for explosive action, thrilling moments, and intense competition 💥

📢 Witness the battle LIVE!
"""

elif "hackathon" in topic_lower or "ai" in topic_lower:

    message = f"""
💻 {topic} is LIVE! 🚀

Join innovators, creators, and developers in an exciting world of technology and creativity 🔥

📢 Build the future with us!
"""

else:

    message = f"""
🚀 {topic} is happening soon!

Get ready for an exciting experience filled with energy and unforgettable moments 🔥
"""

# -----------------------------------
# CHROME SETUP
# -----------------------------------

service = Service(ChromeDriverManager().install())

options = webdriver.ChromeOptions()

options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=service, options=options)

# -----------------------------------
# OPEN WHATSAPP
# -----------------------------------

driver.get("https://web.whatsapp.com")

print("Please scan QR code...")

time.sleep(40)

# -----------------------------------
# LOOP CONTACTS
# -----------------------------------

for number in contacts:

    try:

        print(f"Sending to {number}")

        encoded_message = urllib.parse.quote(message)

        url = f"https://web.whatsapp.com/send?phone={number}&text={encoded_message}"

        driver.get(url)

        time.sleep(15)

        message_box = driver.find_element(
            By.XPATH,
            '//div[@contenteditable="true"][@role="textbox"]'
        )

        message_box.click()

        time.sleep(2)

        message_box.send_keys(Keys.ENTER)

        print(f"✅ Sent to {number}")

        time.sleep(10)

    except Exception as e:

        print(f"❌ Failed for {number}")

        print(e)

print("✅ AI WhatsApp automation completed!")

input("Press Enter to close browser...")