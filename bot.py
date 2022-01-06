import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor, exceptions
from PIL import Image
import pytesseract

API_TOKEN = '5082150067:AAEF9eHOGQT1_iG6k_oCG_zGqkhFHGk3FAs'
channel = '@ok7_bots'
channel_join_link = 'https://t.me/+K4HZ7LZq4SY2NzEy'
admin_id = 880280670
# pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


def subscribe_markup():
    url = types.InlineKeyboardButton('🔗 View channel', url=channel_join_link)
    check = types.InlineKeyboardButton('✅ Confirmation', callback_data='check')
    return types.InlineKeyboardMarkup(resize_keyboard=True, row_width=12).row(url).row(check)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message)
    name = message.chat.first_name
    await message.reply(f'🤖 Hello {name}\! \nWelcome to *Image To Text Bot*\.\n'
                        'Just send me a picture and I will find the text in it', parse_mode='MarkdownV2')


@dp.message_handler(content_types=['photo', 'file'])
async def handle_docs_photo(message: types.Message):
    user_id = message.chat.id
    user_channel_status = await bot.get_chat_member(chat_id=channel, user_id=user_id)
    if user_channel_status.status not in ['left', 'kicked']:
        try:
            await message.photo[-1].download('photo.jpg')
            wait_message = await message.answer('Please wait ...')
            image = 'photo.jpg'
            text = pytesseract.image_to_string(Image.open(image), lang="eng")
            await bot.delete_message(user_id, wait_message.message_id)
            await message.reply(text)
        except exceptions.BadRequest:
            await bot.delete_message(user_id, wait_message.message_id)
            await message.reply('No text found')
    else:
        await message.answer('🤖 Please, subscribe to the channel below to use the bot', reply_markup=subscribe_markup())


@dp.callback_query_handler(text='check')
async def check_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.message.chat.id
    user = callback_query.message.chat.first_name
    user_channel_status = await bot.get_chat_member(chat_id=channel, user_id=user_id)
    if user_channel_status.status in ['left', 'kicked']:
        await bot.answer_callback_query(callback_query.id, "You aren't a member of the channel", show_alert=True)
    else:
        await bot.delete_message(user_id, callback_query.message.message_id)
        await bot.send_message(admin_id, f'[{user}](tg://user?id={user_id}) joined the channel', parse_mode='MarkdownV2')
        await callback_query.message.answer('✅ OK. Now you can now use the bot')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
