import asyncio
import datetime
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from config import token, user_id
from utils import check_news_update

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(maessage: types.Message):
    start_button = ['Все новости', 'Последние 5 новостей', 'Свежие новости']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)

    await maessage.answer('Лента новостей', reply_markup=keyboard)


@dp.message_handler(Text(equals='Все новости'))
async def get_all_news(maessage: types.Message):
    with open('news_dict.json', encoding="utf-8") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        news = f'{hbold(datetime.datetime.fromtimestamp(v["article_date_time"]))}\n' \
               f'{hlink(v["article_title"], v["article_url"])}'

        await maessage.answer(news)


@dp.message_handler(Text(equals='Последние 5 новостей'))
async def get_last_five_news(maessage: types.Message):
    with open('news_dict.json', encoding="utf-8") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = f'{hbold(datetime.datetime.fromtimestamp(v["article_date_time"]))}\n' \
               f'{hlink(v["article_title"], v["article_url"])}'
        await maessage.answer(news)


@dp.message_handler(Text(equals='Свежие новости'))
async def get_fresh_news(maessage: types.Message):
    fresh_news = check_news_update()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items())[-5:]:
            news = f'{hbold(datetime.datetime.fromtimestamp(v["article_date_time"]))}\n' \
                   f'{hlink(v["article_title"], v["article_url"])}'
            await maessage.answer(news)
    else:
        await maessage.answer("Извините Павел Александрович, свежего пока нет.")


async def news_every_hours():
    while True:
        fresh_news = check_news_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items())[-5:]:
                news = f'{hbold(datetime.datetime.fromtimestamp(v["article_date_time"]))}\n' \
                       f'{hlink(v["article_title"], v["article_url"])}'

                await bot.send_message(user_id, news, disable_notification=True)
        else:
            await bot.send_message(user_id, 'Пока тишина, админы спят.', disable_notification=True)

        await asyncio.sleep(2000)


if __name__ == '__main__':
    executor.start_polling(dp)
