import aiohttp

async def get_price(symbol: str):
    """دریافت قیمت از بایننس"""
    symbol = symbol.upper().replace("USDT", "") + "USDT"
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    return float(data['price'])
        except: return None

async def get_fiat_price(base: str, target: str):
    """نرخ تبدیل جفت ارزها"""
    url = f"https://open.er-api.com/v6/latest/{base.upper()}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                data = await response.json()
                return data['rates'].get(target.upper())
        except: return None

async def get_all_fiat_rates():
    """لیست نرخ‌های جهانی شامل ایران"""
    url = "https://open.er-api.com/v6/latest/USD"
    important = ["EUR", "GBP", "TRY", "IRR", "AED", "CNY", "CAD", "AUD", "JPY"]
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                data = await response.json()
                rates = data.get('rates', {})
                return {c: rates[c] for c in important if c in rates}
        except: return None

async def get_crypto_news():
    """دریافت ۵ خبر آخر"""
    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                data = await response.json()
                return data['Data'][:5]
        except: return None