import logging
import yaml
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from bottoken import token

# Объект бота
bot = Bot(token=token)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


# функция отвечающая за распиание
def colel_schedule(pupildict:dict):
    i = 0
    """
    Получаем словарь со списком людей отсортированный по количеству дежурств
    """
    sortedpupils = dict(sorted(pupildict.items(), key=lambda x: x[1]['quantity']))
    print(sortedpupils)
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
        pupildict[i]['quantity'] += 1
    with open('pupils.yaml', 'w') as file:
        documents = yaml.dump(pupildict, file)
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
    try:
        with open('pupils.yaml') as f:
            pupildict = yaml.safe_load(f)
            await message.reply(colel_schedule(pupildict))
    except:
        await message.reply("Добавьте учеников")


@dp.message_handler(lambda message: message.text == "Список учеников")
async def without_puree(message: types.Message):
    # загружаем актуальный список учеников
    with open('pupils.yaml') as f:
        pupildict = yaml.safe_load(f)
    await message.answer(pupildict)


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
