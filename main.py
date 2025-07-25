import requests
import time
import telebot
from bs4 import BeautifulSoup

TOKEN = "8151008836:AAGfdR8BchkGQ210CdAHSx_ksiCctm0vpyc"
CHAT_ID = None  # Автоматически запомним, когда пользователь отправит /start
SESSION_COOKIE = "eyJpdiI6IkZCNXk5eWp5N0FzWWl1R0pzVWF2WUE9PSIsInZhbHVlIjoieUZsbVZ2OU5qc2xMR3dnMENCZ2ZLTWdRNmgyV2dBMjhkU0V3b1FvRVdDb21rMm1IOGVaeng1UUVaSThyejR5UCIsIm1hYyI6ImRhYWEzOGU0MDIzNzZlOGM1ZmJiYjdhNjAzNzNlY2MxMWQyMWY1Y2ZjZjBhZmE0YTc2OGViYWJjOWI0NjE0Y2EifQ%3D%3D"

bot = telebot.TeleBot(TOKEN)

def check_ijevan_date():
    url = "https://roadpolice.am/exam/register"
    cookies = {
        "laravel_session": SESSION_COOKIE
    }
    response = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(response.text, "html.parser")

    dates = soup.find_all("div", class_="available_date")
    for date in dates:
        if "Իջևան" in date.text:
            return date.text.strip()
    return None

@bot.message_handler(commands=['start'])
def start(message):
    global CHAT_ID
    CHAT_ID = message.chat.id
    bot.send_message(message.chat.id, "✅ Բարև, ես սկսում եմ ստուգել Իջևանի գործնական քննության օրերը։")

def main_loop():
    while True:
        if CHAT_ID:
            found = check_ijevan_date()
            if found:
                bot.send_message(CHAT_ID, f"📢 Գտնվեց ազատ օր Իջևանի համար: {found}")
        time.sleep(600)  # 10 րոպե

if name == "__main__":
    import threading
    threading.Thread(target=main_loop).start()
    bot.polling()
