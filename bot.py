import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from PIL import Image
import pytesseract

API_TOKEN = '5082150067:AAEF9eHOGQT1_iG6k_oCG_zGqkhFHGk3FAs'
channel = '@ok7_bots'
channel_join_link = 'https://t.me/+K4HZ7LZq4SY2NzEy'
admin_id = 880280670
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    name = message.chat.first_name
    await message.reply(f'🤖 Hello {name}\! Welcome to *Image To Text Bot*\. '
                        'Just send me the image '
                        'and I will search for it on wikipedia', parse_mode='MarkdownV2')


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: types.Message):
    await message.photo[-1].download('photo.jpg')
    image = 'photo.jpg'
    text = pytesseract.image_to_string(Image.open(image), lang="eng")
    await message.reply(text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
