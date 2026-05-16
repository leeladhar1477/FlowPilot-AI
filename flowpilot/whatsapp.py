from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pyperclip
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException, StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class WhatsAppConfig:
    wait_seconds: int = 60
    login_wait_seconds: int = 180
    user_data_dir: str | None = "browser_profiles/whatsapp"
    keep_browser_open: bool = True


class WhatsAppImageSender:
    """Production-style WhatsApp Web image sender.

    The class deliberately avoids Selenium `send_keys(caption)` for captions.
    ChromeDriver can crash on non-BMP emoji, so captions are inserted through
    the system clipboard and pasted into the media-preview caption box.
    """

    CHAT_BOX_SELECTORS = (
        (By.CSS_SELECTOR, 'footer div[contenteditable="true"][role="textbox"]'),
        (By.XPATH, '//footer//div[@contenteditable="true"][@role="textbox"]'),
        (By.XPATH, '//div[@aria-placeholder="Type a message"][@contenteditable="true"]'),
        (By.XPATH, '//div[@contenteditable="true"][@role="textbox"]'),
    )

    HOME_READY_SELECTORS = (
        (By.CSS_SELECTOR, '#side'),
        (By.CSS_SELECTOR, 'div[aria-label="Chat list"]'),
        (By.XPATH, '//*[@aria-label="Search input textbox" or @aria-label="Search"]'),
    )

    ATTACH_BUTTON_SELECTORS = (
        (By.CSS_SELECTOR, 'button[aria-label="Attach"]'),
        (By.XPATH, '//span[@data-icon="plus-rounded"]/ancestor::*[@role="button" or self::button][1]'),
        (By.XPATH, '//span[@data-icon="clip"]/ancestor::*[@role="button" or self::button][1]'),
        (By.XPATH, '//*[@aria-label="Attach" or @title="Attach"]'),
    )

    FILE_INPUT_SELECTORS = (
        (By.CSS_SELECTOR, 'input[type="file"][accept*="image"]'),
        (By.CSS_SELECTOR, 'input[type="file"][accept*="video"]'),
        (By.CSS_SELECTOR, 'input[type="file"]'),
    )

    CAPTION_BOX_SELECTORS = (
        (By.XPATH, '//div[@role="dialog"]//div[@contenteditable="true"][@role="textbox"]'),
        (By.XPATH, '//div[contains(@aria-label, "Add a caption")][@contenteditable="true"]'),
        (By.XPATH, '//div[contains(@aria-placeholder, "Add a caption")][@contenteditable="true"]'),
        (By.XPATH, '//div[@contenteditable="true"][@role="textbox"]'),
    )

    MEDIA_SEND_SELECTORS = (
        (By.CSS_SELECTOR, 'div[aria-label="Send"][role="button"]'),
        (By.CSS_SELECTOR, 'button[aria-label="Send"]'),
        (By.XPATH, '//div[@role="dialog"]//*[@data-icon="send"]/ancestor::*[@role="button" or self::button][1]'),
        (By.XPATH, '//*[@data-icon="send"]/ancestor::*[@role="button" or self::button][1]'),
    )

    INVALID_PHONE_SELECTORS = (
        (By.XPATH, '//*[contains(text(), "Phone number shared via url is invalid")]'),
        (By.XPATH, '//*[contains(text(), "phone number shared via url is invalid")]'),
        (By.XPATH, '//*[contains(text(), "isn\u2019t on WhatsApp")]'),
        (By.XPATH, '//*[contains(text(), "is not on WhatsApp")]'),
    )

    def __init__(self, config: WhatsAppConfig | None = None) -> None:
        self.config = config or WhatsAppConfig()
        self.driver = self._create_driver()
        self.wait = WebDriverWait(self.driver, self.config.wait_seconds)

    def _create_driver(self) -> WebDriver:
        options = self._build_chrome_options(self.config.user_data_dir)
        service = Service(ChromeDriverManager().install())

        try:
            return webdriver.Chrome(service=service, options=options)
        except SessionNotCreatedException:
            LOGGER.exception(
                "Chrome could not start with profile %r. This usually means the profile is locked by another Chrome window.",
                self.config.user_data_dir,
            )
            fallback_profile = f"browser_profiles/whatsapp_fallback_{int(time.time())}"
            LOGGER.info("Retrying with a fresh temporary automation profile: %s", fallback_profile)
            return webdriver.Chrome(service=service, options=self._build_chrome_options(fallback_profile))

    def _build_chrome_options(self, user_data_dir: str | None) -> webdriver.ChromeOptions:
        options = webdriver.ChromeOptions()
        if self.config.keep_browser_open:
            options.add_experimental_option("detach", True)
        if user_data_dir:
            profile_path = Path(user_data_dir).resolve()
            profile_path.mkdir(parents=True, exist_ok=True)
            options.add_argument(f"--user-data-dir={profile_path}")
            options.add_argument("--profile-directory=Default")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--remote-debugging-port=0")
        options.add_argument("--start-maximized")
        return options

    def open_and_wait_for_login(self) -> None:
        self.driver.get("https://web.whatsapp.com")
        WebDriverWait(self.driver, self.config.login_wait_seconds).until(
            lambda driver: self._first_visible(self.HOME_READY_SELECTORS, timeout=2) is not None
            or driver.find_elements(By.CSS_SELECTOR, 'canvas[aria-label*="Scan"]')
        )

        if self.driver.find_elements(By.CSS_SELECTOR, 'canvas[aria-label*="Scan"]'):
            print("Scan the WhatsApp QR code in Chrome. Waiting for login...")
            WebDriverWait(self.driver, self.config.login_wait_seconds).until(
                lambda _driver: self._first_visible(self.HOME_READY_SELECTORS, timeout=2) is not None
            )

    def send_image_to_many(
        self,
        contacts: Iterable[str],
        image_path: str | os.PathLike[str],
        caption: str,
        delay_between_contacts: float = 8,
    ) -> dict[str, bool]:
        results: dict[str, bool] = {}
        for contact in contacts:
            try:
                self.send_image(contact, image_path, caption)
                results[contact] = True
                LOGGER.info("Image sent to %s", contact)
            except Exception:
                results[contact] = False
                LOGGER.exception("Failed sending image to %s", contact)
                self._save_debug_screenshot(f"failed_{contact}")
            time.sleep(delay_between_contacts)
        return results

    def send_image(self, phone_number: str, image_path: str | os.PathLike[str], caption: str) -> None:
        resolved_image = Path(image_path).resolve()
        if not resolved_image.exists():
            raise FileNotFoundError(f"Image not found: {resolved_image}")

        LOGGER.info("[%s] Opening chat", phone_number)
        self._open_chat(phone_number)
        LOGGER.info("[%s] Clicking attach", phone_number)
        self._click_attach()
        LOGGER.info("[%s] Uploading image: %s", phone_number, resolved_image)
        self._upload_file(resolved_image)
        LOGGER.info("[%s] Waiting for media preview caption box", phone_number)
        caption_box = self._wait_for_media_caption_box()
        LOGGER.info("[%s] Pasting caption", phone_number)
        self._paste_text(caption_box, caption)
        LOGGER.info("[%s] Sending media", phone_number)
        self._click_media_send()
        self._wait_until_preview_closes()

    def _open_chat(self, phone_number: str) -> None:
        normalized = "".join(ch for ch in phone_number if ch.isdigit())
        self.driver.get(f"https://web.whatsapp.com/send?phone={normalized}&app_absent=0")

        chat_or_invalid = self.wait.until(
            lambda _driver: self._first_visible(self.CHAT_BOX_SELECTORS, timeout=2)
            or self._first_visible(self.INVALID_PHONE_SELECTORS, timeout=2)
        )

        if self._element_matches_any(chat_or_invalid, self.INVALID_PHONE_SELECTORS):
            raise ValueError(f"WhatsApp rejected this phone number: {phone_number}")

    def _wait_for_chat_ready(self) -> None:
        self.wait.until(lambda _driver: self._first_visible(self.CHAT_BOX_SELECTORS, timeout=2))

    def _click_attach(self) -> None:
        button = self._first_clickable(self.ATTACH_BUTTON_SELECTORS)
        self._safe_click(button)

    def _upload_file(self, image_path: Path) -> None:
        file_input = self._first_present(self.FILE_INPUT_SELECTORS)
        file_input.send_keys(str(image_path))

    def _wait_for_media_caption_box(self) -> WebElement:
        self.wait.until(lambda _driver: self._first_clickable(self.MEDIA_SEND_SELECTORS, timeout=2))

        def find_caption_box(_driver: WebDriver) -> WebElement | bool:
            candidates = self._visible_elements(self.CAPTION_BOX_SELECTORS)
            caption_candidates = [
                item
                for item in candidates
                if "caption" in (
                    (item.get_attribute("aria-label") or "")
                    + " "
                    + (item.get_attribute("aria-placeholder") or "")
                    + " "
                    + (item.get_attribute("data-placeholder") or "")
                ).lower()
            ]
            if caption_candidates:
                return caption_candidates[-1]
            return candidates[-1] if candidates else False

        return self.wait.until(find_caption_box)

    def _click_media_send(self) -> None:
        visible_send_buttons = self._visible_elements(self.MEDIA_SEND_SELECTORS)
        send_button = visible_send_buttons[-1] if visible_send_buttons else self._first_clickable(self.MEDIA_SEND_SELECTORS)
        self._safe_click(send_button)

    def _wait_until_preview_closes(self) -> None:
        try:
            WebDriverWait(self.driver, 20).until_not(
                lambda _driver: self._visible_elements(self.MEDIA_SEND_SELECTORS)
            )
        except TimeoutException:
            LOGGER.warning("Media preview did not close within timeout; message may still have sent.")

    def _paste_text(self, element: WebElement, text: str) -> None:
        pyperclip.copy(text)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self._safe_click(element)
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()

        try:
            WebDriverWait(self.driver, 10).until(
                lambda _driver: (element.text or element.get_attribute("textContent") or "").strip()
            )
        except (StaleElementReferenceException, TimeoutException):
            LOGGER.debug("Caption text verification skipped because the preview element changed.")

    def _safe_click(self, element: WebElement) -> None:
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    def _first_clickable(self, selectors: tuple[tuple[str, str], ...], timeout: int | None = None) -> WebElement:
        last_error: Exception | None = None
        for selector in selectors:
            try:
                return WebDriverWait(self.driver, timeout or self.config.wait_seconds).until(
                    EC.element_to_be_clickable(selector)
                )
            except Exception as exc:
                last_error = exc
        raise TimeoutException(f"No clickable element found for selectors: {selectors}") from last_error

    def _first_present(self, selectors: tuple[tuple[str, str], ...], timeout: int | None = None) -> WebElement:
        last_error: Exception | None = None
        for selector in selectors:
            try:
                return WebDriverWait(self.driver, timeout or self.config.wait_seconds).until(
                    EC.presence_of_element_located(selector)
                )
            except Exception as exc:
                last_error = exc
        raise TimeoutException(f"No present element found for selectors: {selectors}") from last_error

    def _first_visible(self, selectors: tuple[tuple[str, str], ...], timeout: int | None = None) -> WebElement | None:
        for selector in selectors:
            try:
                return WebDriverWait(self.driver, timeout or self.config.wait_seconds).until(
                    EC.visibility_of_element_located(selector)
                )
            except Exception:
                continue
        return None

    def _visible_elements(self, selectors: tuple[tuple[str, str], ...]) -> list[WebElement]:
        elements: list[WebElement] = []
        for by, value in selectors:
            for element in self.driver.find_elements(by, value):
                try:
                    if element.is_displayed():
                        elements.append(element)
                except StaleElementReferenceException:
                    continue
        return elements

    def _element_matches_any(self, element: WebElement, selectors: tuple[tuple[str, str], ...]) -> bool:
        for by, value in selectors:
            try:
                if element in self.driver.find_elements(by, value):
                    return True
            except StaleElementReferenceException:
                return False
        return False

    def _save_debug_screenshot(self, label: str) -> None:
        debug_dir = Path("logs") / "screenshots"
        debug_dir.mkdir(parents=True, exist_ok=True)
        safe_label = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in label)
        screenshot_path = debug_dir / f"{safe_label}_{int(time.time())}.png"
        try:
            self.driver.save_screenshot(str(screenshot_path))
            LOGGER.info("Saved debug screenshot: %s", screenshot_path)
        except Exception:
            LOGGER.exception("Could not save debug screenshot")
