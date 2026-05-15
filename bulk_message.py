from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse
import time

# -----------------------------------
# CONTACT LIST
# -----------------------------------

contacts = [
    "916305519180",
    "916281363667",
    "919346672887"
]

# -----------------------------------
# MESSAGE
# -----------------------------------

message = """
🚀 Hello from FlowPilot AI!

Bulk WhatsApp automation successful ✅
"""

# -----------------------------------
# CHROME SETUP
# -----------------------------------

service = Service(ChromeDriverManager().install())

options = webdriver.ChromeOptions()

# Keep browser open
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=service, options=options)

# -----------------------------------
# OPEN WHATSAPP WEB
# -----------------------------------

driver.get("https://web.whatsapp.com")

print("Please scan QR code...")

# IMPORTANT:
# Wait for WhatsApp to fully load chats
time.sleep(40)

# -----------------------------------
# LOOP THROUGH CONTACTS
# -----------------------------------

for number in contacts:

    try:

        print(f"\nOpening chat for {number}")

        # Encode message
        encoded_message = urllib.parse.quote(message)

        # Open direct chat
        url = f"https://web.whatsapp.com/send?phone={number}&text={encoded_message}"

        driver.get(url)

        print("Waiting for chat to load...")

        # Wait for chat loading
        time.sleep(15)

        # -----------------------------------
        # FIND MESSAGE BOX
        # -----------------------------------

        message_box = driver.find_element(
            By.XPATH,
            '//div[@contenteditable="true"][@role="textbox"]'
        )

        # Click message box
        message_box.click()

        time.sleep(2)

        # -----------------------------------
        # SEND MESSAGE
        # -----------------------------------

        message_box.send_keys(Keys.ENTER)

        print(f"✅ Message sent to {number}")

        # Delay before next contact
        time.sleep(10)

    except Exception as e:

        print(f"❌ Failed for {number}")

        print(e)

        # Wait before continuing
        time.sleep(5)

print("\n✅ Bulk messaging completed!")

input("Press Enter to close browser...")