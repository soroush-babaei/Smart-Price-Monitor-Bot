from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📊 Track Price")],
        [KeyboardButton(text="🛠 ابزارهای کاربردی")]
    ], resize_keyboard=True)

def categories_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="💎 کریپتوکارنسی")],
        [KeyboardButton(text="💵 ارزهای پولی (Fiat)")],
        [KeyboardButton(text="🔙 بازگشت به منوی اصلی")]
    ], resize_keyboard=True)

def crypto_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="BTC 🟠"), KeyboardButton(text="ETH 🔵")],
        [KeyboardButton(text="SOL 🟣"), KeyboardButton(text="DOGE 🟡")],
        [KeyboardButton(text="🔍 جستجوی سایر ارزها")],
        [KeyboardButton(text="🔙 بازگشت")]
    ], resize_keyboard=True)

def fiat_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📊 لیست کامل نرخ‌ها")],
        [KeyboardButton(text="🔍 جستجوی جفت ارز")],
        [KeyboardButton(text="🔙 بازگشت")]
    ], resize_keyboard=True)

def tools_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📰 اخبار فوری")],
        [KeyboardButton(text="🧮 ماشین حساب")],
        [KeyboardButton(text="🔙 بازگشت")]
    ], resize_keyboard=True)