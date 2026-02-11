import re
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils import *
from services import *

router = Router()

class Form(StatesGroup):
    waiting_for_crypto_search = State()
    waiting_for_fiat_search = State()
    waiting_for_calc = State()

@router.message(Command("start"))
@router.message(F.text == "🔙 بازگشت به منوی اصلی")
async def start_cmd(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("🚀 خوش آمدید! انتخاب کنید:", reply_markup=main_menu())

@router.message(F.text == "📊 Track Price")
@router.message(F.text == "🔙 بازگشت")
async def track_price_start(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("دسته مورد نظر را انتخاب کنید:", reply_markup=categories_keyboard())

# --- کریپتوکارنسی ---
@router.message(F.text == "💎 کریپتوکارنسی")
async def crypto_menu(msg: Message):
    await msg.answer("ارز مورد نظر یا جستجو را انتخاب کنید:", reply_markup=crypto_keyboard())

@router.message(F.text.in_({"BTC 🟠", "ETH 🔵", "SOL 🟣", "DOGE 🟡"}))
async def quick_crypto(msg: Message):
    symbol = msg.text.split()[0]
    price = await get_price(symbol)
    if price:
        await msg.answer(f"💰 **{symbol}**: `${price:,.2f}`\n📊 [نمودار زنده](https://www.tradingview.com/symbols/{symbol}USDT/)")
    else:
        await msg.answer("❌ خطا در دریافت قیمت. احتمالاً مشکل از IP سرور است.")

@router.message(F.text == "🔍 جستجوی سایر ارزها")
async def search_crypto_init(msg: Message, state: FSMContext):
    await state.set_state(Form.waiting_for_crypto_search)
    await msg.answer("⌨️ نام ارز را وارد کنید (مثلاً: ADA):")

@router.message(Form.waiting_for_crypto_search)
async def search_crypto_proc(msg: Message, state: FSMContext):
    symbol = msg.text.upper().strip()
    p = await get_price(symbol)
    if p:
        await msg.answer(f"💰 **{symbol}**: `${p:,.2f}`")
        await state.clear()
    else:
        await msg.answer("❌ یافت نشد. نام صحیح را بفرستید:")

# --- ارزهای پولی ---
@router.message(F.text == "💵 ارزهای پولی (Fiat)")
async def fiat_menu(msg: Message):
    await msg.answer("انتخاب کنید:", reply_markup=fiat_keyboard())

@router.message(F.text == "📊 لیست کامل نرخ‌ها")
async def all_fiat_list(msg: Message):
    rates = await get_all_fiat_rates()
    if rates:
        txt = "📜 **نرخ ارزها (پایه 1 دلار):**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        flags = {"EUR":"🇪🇺", "GBP":"🇬🇧", "TRY":"🇹🇷", "IRR":"🇮🇷", "AED":"🇦🇪", "CNY":"🇨🇳", "CAD":"🇨🇦", "AUD":"🇦🇺", "JPY":"🇯🇵"}
        for code, rate in rates.items():
            txt += f"{flags.get(code, '🏳️')} {code}: `{rate:,.2f}`\n"
        await msg.answer(txt)
    else:
        await msg.answer("❌ خطا در دریافت نرخ‌ها.")

@router.message(F.text == "🔍 جستجوی جفت ارز")
async def search_fiat_init(msg: Message, state: FSMContext):
    await state.set_state(Form.waiting_for_fiat_search)
    await msg.answer("⌨️ جفت ارز را بفرستید (مثلاً: USD-TRY):")

@router.message(Form.waiting_for_fiat_search)
async def search_fiat_proc(msg: Message, state: FSMContext):
    try:
        parts = msg.text.upper().replace("/", "-").replace(" ", "-").split("-")
        r = await get_fiat_price(parts[0], parts[1])
        if r:
            await msg.answer(f"💹 نرخ **{parts[0]}/{parts[1]}**: `{r:.4f}`")
            await state.clear()
    except:
        await msg.answer("❌ مثال: USD-TRY")

# --- ابزارها ---
@router.message(F.text == "🛠 ابزارهای کاربردی")
async def tools_menu(msg: Message):
    await msg.answer("ابزار مورد نظر:", reply_markup=tools_keyboard())

@router.message(F.text == "📰 اخبار فوری")
async def news_proc(msg: Message):
    news = await get_crypto_news()
    if news:
        for n in news:
            await msg.answer(f"📰 **{n['title']}**\n[لینک خبر]({n['url']})")
    else:
        await msg.answer("❌ موفق به دریافت اخبار نشدیم.")

@router.message(F.text == "🧮 ماشین حساب")
async def calc_init(msg: Message, state: FSMContext):
    await state.set_state(Form.waiting_for_calc)
    await msg.answer("⌨️ مقدار و نام ارز را وارد کنید (مثلاً: 1.5 BTC):")

@router.message(Form.waiting_for_calc)
async def calc_proc(msg: Message, state: FSMContext):
    try:
        num = float(re.findall(r"\d+\.?\d*", msg.text)[0])
        sym = re.findall(r"[A-Z]{2,}", msg.text.upper())[0]
        p = await get_price(sym)
        if p:
            await msg.answer(f"💰 ارزش **{num} {sym}**: **${num*p:,.2f}**")
            await state.clear()
    except:
        await msg.answer("❌ مثال: 1.5 BTC")