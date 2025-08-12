from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    btn = KeyboardButton(text="📚 Kursga ro‘yxatdan o‘tish")
    markup = ReplyKeyboardMarkup(keyboard=[[btn]], resize_keyboard=True)
    await message.answer(
        "Assalomu alaykum!\n"
        "Xush kelibsiz! Matematika o‘qituvchisi **Zokirov Zokirjon** ning "
        "\"Matematika kursi\"ga ro‘yxatdan o‘tish uchun ushbu tugmani bosing.",
        reply_markup=markup
    )

@dp.message(lambda msg: msg.text == "📚 Kursga ro‘yxatdan o‘tish")
async def ask_name(message: types.Message):
    await message.answer("Iltimos, ism va familiyangizni kiriting:")
    dp.message.register(get_name)

async def get_name(message: types.Message):
    name = message.text
    contact_button = KeyboardButton("📞 Telefon raqamni yuborish", request_contact=True)
    markup = ReplyKeyboardMarkup(keyboard=[[contact_button]], resize_keyboard=True)
    message.bot_data["name"] = name
    await message.answer("Endi telefon raqamingizni yuboring:", reply_markup=markup)
    dp.message.register(get_contact)

async def get_contact(message: types.Message):
    name = message.bot_data.get("name", "Noma'lum")
    phone = message.contact.phone_number
    await bot.send_message(ADMIN_ID, f"📥 Yangi ro‘yxatdan o‘tuvchi:\n👤 Ism: {name}\n📞 Tel: {phone}")
    await message.answer("✅ Rahmat! Siz bilan tez orada aloqaga chiqamiz.", reply_markup=types.ReplyKeyboardRemove())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())