import os
import requests
from playwright.sync_api import Playwright, sync_playwright, TimeoutError

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=payload)

def run(playwright: Playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://termine.staedteregion-aachen.de/auslaenderamt/")
    page.get_by_role("button", name="Aufenthaltsangelegenheiten").click()
    page.get_by_role("tab", name="RWTH - Außenstelle Super C").click()
    page.get_by_role("button", name="Erhöhen der Anzahl des Anliegens RWTH Studenten").click()
    page.get_by_role("button", name="Weiter").click()
    page.get_by_role("button", name="OK", exact=True).click()
    page.get_by_role("button", name="Weiter").click()

    try:
        page.get_by_role("heading", name="Kein freier Termin verfügbar", exact=True).wait_for(timeout=3000)
        print("❌ 没有空位")
        send_telegram_message("test")
    except TimeoutError:
        print("✅ 现在可能有空位，发送通知")
        send_telegram_message("📢 现在有空位了！请尽快去预约：https://termine.staedteregion-aachen.de/auslaenderamt/")

    context.close()
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
