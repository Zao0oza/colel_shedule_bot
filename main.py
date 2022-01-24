from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from bottoken import token, google_url
import gspread


gc = gspread.service_account(filename='regal-eon-313211-848c0cdd83c0.json') # ключ для google api

# Объект бота
bot = Bot(token=token)
# Диспетчер для бота
dp = Dispatcher(bot)


# функция отвечающая за распиание
def colel_schedule():
    pupilres = []
    """
    Получаем словарь и сортируем по списку дежурств
    Убираем отсутсвующих
    """
    try:
        wks = gc.open_by_url(
            google_url)# url google документа
        worksheet = wks.get_worksheet(0)
        list_of_dicts = worksheet.get_all_values()
        pupildict = {v: [k, j] for v, k, j in list_of_dicts[1:]}
        sortedpupils = dict(sorted(pupildict.items(), key=lambda x: x[1][0]))
        for i in list(sortedpupils.keys()):
            if sortedpupils[i][1] == "Нет":
                pupilres.append(i)
                if len(pupilres) == 5:
                    break
        """
        Проверям сколько хватает ли людей на 5 дней
        если нет добавляем доаполнительное дежурство первому ,
        второму и т.д смотря сколько не хватает
        """
        if len(pupilres) < 5:
            i = 0
            while len(pupilres) < 5:
                pupilres.append(pupilres[i])
                i += 1
        """
        Добавляем дежурство выбранным ученикам
        Сохраняем данные в таблице
        """
        for i in pupilres:
            cell = worksheet.find(i)
            val = int(worksheet.cell(cell.row, cell.col + 1).value) + 1
            worksheet.update(f'R{cell.row}C{cell.col + 1}', val)
        return f"Воскресенье: {pupilres[0]}\nПонедельник:{pupilres[1]}\nВторник: {pupilres[2]}\nСреда: {pupilres[3]}\nЧетверг: {pupilres[4]}\n"
    except :
        return "проверьте список учеников!"


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Расписание", "Список учеников"]
    keyboard.add(*buttons)
    await message.answer("Что вы хотите?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Расписание"))
async def with_puree(message: types.Message):
    # загружаем актуальный список учеников
    await message.answer(colel_schedule())
    # await message.reply("Добавьте учеников")


@dp.message_handler(lambda message: message.text == "Список учеников")
async def without_puree(message: types.Message):
    # загружаем актуальный список учеников
    await message.answer(
        'https://docs.google.com/spreadsheets/d/1ljIQbUyL_RMii47joDgWRfXr4q15e4mSw1oA1ZxI8D0/edit#gid=0')
    # await message.answer("Добавьте учеников")


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
