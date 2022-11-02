from imaplib import Commands
from turtle import end_fill
import requests
from bs4 import BeautifulSoup as BS
import lxml
from deep_translator import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

m = requests.get('https://sinoptik.ua/погода-ташкент')
html_t = BS(m.content, "html.parser")
#csrf = 'c75bd288f5787d6bcbe1d1a5f30ad502a0e7c02f'

d = requests.get('https://nbu.uz/uz/exchange-rates/')
dol = BS(d.content, 'html.parser')

b = html_t.find('div', class_="tabs").find_all('div')[1].text.strip()
#d = html_t.find("div", class_="kursdata")

sana = GoogleTranslator(source='auto', target='uz').translate(b[0:20])
dollar = dol.find('div', class_='kursdata').find_all('td')[2].text
#print('1 AQSH dollari(USD): ',dollar)

yevro = dol.find('div', class_='kursdata').find_all('td')[5].text
#print('1 Yevro(EUR): ', yevro)

rubl = dol.find('div', class_='kursdata').find_all('td')[8].text
#print('1 Rossiya rubli(RUB): ', rubl)

def city():
    return [
        [InlineKeyboardButton("Dollar kursi", callback_data=f"01")],
        [InlineKeyboardButton("Yevro kursi", callback_data=f"02")],
        [InlineKeyboardButton("Rubl kursi", callback_data=f"03")]
    ]

def back():
    return [
        [InlineKeyboardButton("Orqaga", callback_data=f"back1")]
    ]

def inline_handlerlar(update, context):
    query = update.callback_query
    data = query.data.split("_")

    if data[0] == "01":
        query.message.edit_text(f"Bugungi sana: {sana} \n1 AQSH dollari(USD): {dollar} \n Manzilimiz: @valyuta_infobot",
                                reply_markup=InlineKeyboardMarkup(back()))
    elif data[0] == "02":
        query.message.edit_text(f"Bugungi sana: {sana} \n1 Yevro(EUR):  {yevro} \n Manzilimiz: @valyuta_infobot",
                                reply_markup=InlineKeyboardMarkup(back()))
    elif data[0] == "03":
        query.message.edit_text(f"Bugungi sana: {sana} \n1 Rossiya rubli(RUB): {rubl} \n Manzilimiz: @valyuta_infobot",
                                reply_markup=InlineKeyboardMarkup(back()))


    elif data[0] == 'back1':
        query.message.edit_text(
            f"Bu yerdan valyuta kursini tanlang 👇",
            reply_markup=InlineKeyboardMarkup(city()))

def start(update, context):
    user = update.message.from_user
    update.message.reply_text(f"""Salom {user.first_name} 🖐🏼\nBu yerdan valyuta turini tanlang 👇""",
                              reply_markup=InlineKeyboardMarkup(city()))


def main():
    Token = "5692146863:AAF0XSa8Zmwbqbl-kkGPtUntuE9n0dDtAts"
    updater = Updater(Token)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(inline_handlerlar))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
