import logging
import yaml
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from bottoken import token
import gspread

gc = gspread.service_account(filename='regal-eon-313211-848c0cdd83c0.json')

# Объект бота
bot = Bot(token=token)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


def get_pupils():
    wks = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1ljIQbUyL_RMii47joDgWRfXr4q15e4mSw1oA1ZxI8D0/edit#gid=0')
    worksheet = wks.get_worksheet(0)
    list_of_dicts = worksheet.get_all_values()
    pupildict = {v: [k, j] for v, k, j in list_of_dicts[1:]}
    return pupildict


# функция отвечающая за распиание
def colel_schedule():
    i = 0
    """
    Получаем словарь и сортируем по списку дежурств
    """
    sortedpupils = dict(sorted(get_pupils().items(), key=lambda x: x[1][0]))
    pupilres = list(sortedpupils.keys())[0:5]
    """
    Проверям сколько хватает ли людей на 5 дней
    если нет добавляем доаполнительное дежурство первому ,
    второму и т.д смотря сколько не хватает
    """
    if len(pupilres) < 5:
        while len(pupilres) < 5:
            pupilres.append(pupilres[i])
            i += 1
    """
    Добавляем дежурство выбранным ученикам
    Записываем их в файл
    """
    for i in pupilres:
        wks = gc.open_by_url(
            'https://docs.google.com/spreadsheets/d/1ljIQbUyL_RMii47joDgWRfXr4q15e4mSw1oA1ZxI8D0/edit#gid=0')
        worksheet = wks.get_worksheet(0)
        cell = worksheet.find(i)
        val=int(worksheet.cell(cell.row, cell.col+1).value)+1
        worksheet.update(f'R{cell.row}C{cell.col + 1}', val)
    return pupilres


# Хэндлер на команду /test1
@dp.message_handler(commands="test1")
async def cmd_test1(message: types.Message):
    await message.reply("Test 1")


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Расписание", "Список учеников"]
    keyboard.add(*buttons)
    await message.answer("Что вы хотите?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Расписание"))
async def with_puree(message: types.Message):
    # загружаем актуальный список учеников
    await message.reply(colel_schedule())
    #await message.reply("Добавьте учеников")


@dp.message_handler(lambda message: message.text == "Список учеников")
async def without_puree(message: types.Message):
    # загружаем актуальный список учеников
    await message.answer(get_pupils())
    #await message.answer("Добавьте учеников")


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
