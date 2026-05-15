from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse
import time

# -----------------------------------
# PHONE NUMBER
# -----------------------------------

phone_number = "916281363667"

message = """
🚀 Hello from FlowPilot AI!

WhatsApp automation successful ✅
"""

# -----------------------------------
# ENCODE MESSAGE
# -----------------------------------

encoded_message = urllib.parse.quote(message)

# -----------------------------------
# CHROME SETUP
# -----------------------------------

service = Service(ChromeDriverManager().install())

options = webdriver.ChromeOptions()

options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=service, options=options)

# -----------------------------------
# OPEN WHATSAPP CHAT
# -----------------------------------

url = f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}"

driver.get(url)

print("Please scan QR code if needed...")

# -----------------------------------
# WAIT FOR MESSAGE BOX
# -----------------------------------

wait = WebDriverWait(driver, 120)

message_box = wait.until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            '//div[@aria-placeholder="Type a message"][@contenteditable="true"]'
        )
    )
)

print("✅ Chat loaded!")

time.sleep(2)

# -----------------------------------
# CLICK MESSAGE BOX
# -----------------------------------

message_box.click()

time.sleep(1)

# -----------------------------------
# SEND MESSAGE
# -----------------------------------

message_box.send_keys(Keys.ENTER)

print("✅ Message sent successfully!")

input("Press Enter to close browser...")