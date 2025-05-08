import time
import requests
from playwright.sync_api import Playwright, sync_playwright, TimeoutError

TELEGRAM_BOT_TOKEN = '7082166080:AAFQiHexgZZHkv-80uMtOwOu59_vuUURrig'
TELEGRAM_CHAT_ID = '6443289918'

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)

def check_rwth(page):
    print("🔍 检查 RWTH 学生预约...")
    page.goto("https://termine.staedteregion-aachen.de/auslaenderamt/")
    page.get_by_role("button", name="Aufenthaltsangelegenheiten").click()
    page.get_by_role("tab", name="RWTH - Außenstelle Super C").click()
    page.get_by_role("button", name="Erhöhen der Anzahl des Anliegens RWTH Studenten").click()
    page.get_by_role("button", name="Weiter").click()
    page.get_by_role("button", name="OK", exact=True).click()
    page.get_by_role("button", name="Weiter").click()

    try:
        page.get_by_role("heading", name="Kein freier Termin verfügbar", exact=True).wait_for(timeout=3000)
        print("❌ RWTH 无空位")
    except TimeoutError:
        print("✅ RWTH 有空位，发送通知")
        send_telegram_message("🎓 RWTH 现在有空位了！快预约：https://termine.staedteregion-aachen.de/auslaenderamt/")

def check_team1(page):
    print("🔍 检查 Team 1（Erteilung/Verlängerung Aufenthalt）预约...")
    page.goto("https://termine.staedteregion-aachen.de/auslaenderamt/")
    page.get_by_role("button", name="Aufenthaltsangelegenheiten").click()
    page.get_by_role("tab", name="Aufenthalt", exact=True).click()
    page.get_by_role("button", name="Erhöhen der Anzahl des Anliegens Erteilung/Verlängerung Aufenthalt - Nachname: A - Z (Team 1)", exact=True).click()
    page.get_by_role("button", name="Weiter").click()
    page.get_by_role("button", name="OK", exact=True).click()
    page.get_by_role("button", name="Weiter").click()

    try:
        page.get_by_role("heading", name="Kein freier Termin verfügbar", exact=True).wait_for(timeout=3000)
        print("❌ Team 1 无空位")
    except TimeoutError:
        print("✅ Team 1 有空位，发送通知")
        send_telegram_message("🔥 Team 1 现在有空位了！快预约：https://termine.staedteregion-aachen.de/auslaenderamt/")

def run(playwright: Playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        check_rwth(page)
        check_team1(page)
    finally:
        context.close()
        browser.close()

if __name__ == "__main__":
    while True:
        with sync_playwright() as playwright:
            run(playwright)
        time.sleep(30)
