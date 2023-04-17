from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hlink
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv
import emoji, sqlite3, time, os
load_dotenv()
bot = Bot("TOKEN")
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(
        f'Привет, {message.from_user.first_name + emoji.emojize(":hand_with_fingers_splayed:")} \nЯ бот GameSearch ищу игры для тебя{emoji.emojize(":red_heart:")} \n'
        f'Введи название игры для поиска {emoji.emojize(":video_game:")}')


@dp.message_handler(Text)
async def f(message: types.Message):
    counter = 0
    if len(message.text) < 4:
        await message.answer('Такое количество символов недопустимо')
    else:
        game_name = (f"%{message.text}%",)
        with sqlite3.connect('C:/Users/Евгений/PycharmProjects/Test_Scrap/games.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT * from games where Name LIKE ?""", game_name)
            records = cursor.fetchall()

            if records == []:
                await message.answer("Введено неправильное название,\nили этой игры у меня нет")
            else:
                for game in records:
                    await message.answer(f"Название: {hlink(title=game[1], url=game[3])} \nЦена: {game[2]} ",
                                         parse_mode="html")
                    counter += 1

                    if counter % 10 == 0:
                        time.sleep(10)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
