
from telegram import  ReplyKeyboardMarkup , ReplyKeyboardRemove, KeyboardButton


def olimpiada():
    return ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🏅 Olimpiada natijalarini ko'rish 🏅")
        ],
    
    ],
    resize_keyboard=True, one_time_keyboard=True
)


def telfon_raqam():
    return ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Kontaktni yuborish 📱", request_contact=True), 
        ],
    
    ],
    resize_keyboard=True, one_time_keyboard=True, 
)