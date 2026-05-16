import customtkinter as ctk
from tkinter import filedialog

from telegram import Bot
import asyncio

from datetime import datetime

# -----------------------------------
# APP SETTINGS
# -----------------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# -----------------------------------
# MAIN WINDOW
# -----------------------------------

app = ctk.CTk()

app.title("FlowPilot AI")

# FULLSCREEN
app.state("zoomed")

# Allow resizing
app.resizable(True, True)

# -----------------------------------
# TELEGRAM SETTINGS
# -----------------------------------

TOKEN = "8930206290:AAGCdq34sOoDNPTb5Qadlk81RBjLzGDHTRg"

CHAT_ID = "6532543741"

# -----------------------------------
# TITLE
# -----------------------------------

header = ctk.CTkLabel(
    app,
    text="FlowPilot AI Campaign Dashboard",
    font=("Arial", 32, "bold")
)

header.pack(pady=20)

# -----------------------------------
# EVENT TOPIC
# -----------------------------------

label_topic = ctk.CTkLabel(
    app,
    text="Enter Event Topic",
    font=("Arial", 20)
)

label_topic.pack()

entry_topic = ctk.CTkEntry(
    app,
    width=600,
    height=45,
    placeholder_text="Example: Cricket Tournament"
)

entry_topic.pack(pady=10)

# -----------------------------------
# CATEGORY DROPDOWN
# -----------------------------------

categories = [
    "Cricket",
    "Boxing",
    "Music",
    "Anime",
    "Hackathon",
    "Gaming",
    "Dance",
    "College Fest"
]

category_menu = ctk.CTkOptionMenu(
    app,
    values=categories,
    width=350,
    height=40
)

category_menu.pack(pady=10)

# -----------------------------------
# IMAGE SECTION
# -----------------------------------

selected_image = ""

image_label = ctk.CTkLabel(
    app,
    text="No Image Selected",
    font=("Arial", 16)
)

image_label.pack(pady=10)

# -----------------------------------
# IMAGE PICKER
# -----------------------------------

def upload_image():

    global selected_image

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )

    if file_path:

        selected_image = file_path

        image_label.configure(
            text=f"Selected: {file_path.split('/')[-1]}"
        )

# -----------------------------------
# UPLOAD BUTTON
# -----------------------------------

upload_btn = ctk.CTkButton(
    app,
    text="Upload Poster",
    command=upload_image,
    height=45,
    width=250,
    font=("Arial", 18)
)

upload_btn.pack(pady=10)

# -----------------------------------
# CAPTION BOX
# -----------------------------------

caption_box = ctk.CTkTextbox(
    app,
    width=1000,
    height=220,
    font=("Arial", 18)
)

caption_box.pack(pady=20)

# -----------------------------------
# STATUS LABEL
# -----------------------------------

status_label = ctk.CTkLabel(
    app,
    text="Status: Waiting...",
    font=("Arial", 16)
)

status_label.pack(pady=10)

# -----------------------------------
# GENERATE CAPTION
# -----------------------------------

def generate_caption():

    topic = entry_topic.get()

    category = category_menu.get()

    caption = f"""
🔥 {topic.upper()} IS HERE! 🔥

Get ready for an unforgettable {category} experience packed with excitement, energy, and entertainment! 🚀

✨ Event Highlights:
🏆 Competitive Atmosphere
🔥 Exciting Moments
📣 Crowd Energy
🎯 Amazing Experience
💥 Non-stop Fun

👑 Bring your squad and enjoy the ultimate event experience!

#FlowPilotAI #{category.replace(' ', '')}
"""

    caption_box.delete("1.0", "end")

    caption_box.insert("end", caption)

# -----------------------------------
# SAVE CAMPAIGN LOG
# -----------------------------------

def save_log(status):

    topic = entry_topic.get()

    category = category_menu.get()

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    log_text = f"""
====================================

Campaign Status: {status}

Topic: {topic}

Category: {category}

Time: {current_time}

Image: {selected_image}

====================================
"""

    with open(
        "logs/campaign_logs.txt",
        "a",
        encoding="utf-8"
    ) as file:

        file.write(log_text)

# -----------------------------------
# TELEGRAM CAMPAIGN
# -----------------------------------

async def telegram_campaign():

    global selected_image

    caption = caption_box.get("1.0", "end")

    bot = Bot(token=TOKEN)

    with open(selected_image, "rb") as photo:

        await bot.send_photo(
            chat_id=CHAT_ID,
            photo=photo,
            caption=caption
        )

    print("Campaign sent successfully!")

    status_label.configure(
        text="Status: Campaign Sent Successfully!",
        text_color="lightgreen"
    )

    save_log("SUCCESS")

# -----------------------------------
# SEND BUTTON FUNCTION
# -----------------------------------

def send_campaign():

    if selected_image == "":

        status_label.configure(
            text="Status: Please upload image first!",
            text_color="red"
        )

        return

    try:

        asyncio.run(
            telegram_campaign()
        )

    except Exception as e:

        print(e)

        status_label.configure(
            text="Status: Campaign Failed!",
            text_color="red"
        )

        save_log("FAILED")

# -----------------------------------
# GENERATE BUTTON
# -----------------------------------

generate_btn = ctk.CTkButton(
    app,
    text="Generate Campaign Caption",
    command=generate_caption,
    height=50,
    width=320,
    font=("Arial", 20, "bold")
)

generate_btn.pack(pady=10)

# -----------------------------------
# SEND TELEGRAM BUTTON
# -----------------------------------

send_btn = ctk.CTkButton(
    app,
    text="Send Telegram Campaign",
    command=send_campaign,
    height=50,
    width=320,
    font=("Arial", 20, "bold"),
    fg_color="green",
    hover_color="darkgreen"
)

send_btn.pack(pady=20)

# -----------------------------------
# RUN APP
# -----------------------------------

app.mainloop()