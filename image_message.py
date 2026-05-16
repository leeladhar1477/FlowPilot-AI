import logging
import os

from flowpilot.whatsapp import WhatsAppConfig, WhatsAppImageSender


CONTACTS = [
    "916305519180",
    "916281363667",
]

IMAGE_PATH = os.path.abspath("images/cric.jpg")

CAPTION = """
CRICKET TOURNAMENT IS HERE!

Get ready for thrilling matches, explosive sixes, unforgettable wickets and crowd energy.

Competitive Teams | Intense Rivalries | Big Hits | Non-stop Entertainment

Don't miss the biggest cricket event of the season!
""".strip()


def main() -> None:
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/image_campaign.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    sender = WhatsAppImageSender(
        WhatsAppConfig(
            wait_seconds=60,
            login_wait_seconds=180,
            user_data_dir="browser_profiles/whatsapp",
            keep_browser_open=True,
        )
    )

    sender.open_and_wait_for_login()
    results = sender.send_image_to_many(CONTACTS, IMAGE_PATH, CAPTION)

    successful = sum(1 for sent in results.values() if sent)
    failed = len(results) - successful
    print(f"\nCampaign finished: {successful} sent, {failed} failed")


if __name__ == "__main__":
    main()
