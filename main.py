from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from bottoken import token, google_url
import gspread
import datetime
import yaml

gc = gspread.service_account(filename='regal-eon-313211-848c0cdd83c0.json')  # ключ для google api

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
            google_url)  # url google документа
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
        result = pupilres[0:5]
        result.insert(0, datetime.date.today())
        with open('store_file.yaml', 'a') as f:
            yaml.dump({datetime.datetime.now(): result}, f, default_flow_style=False, allow_unicode=True)

        return result
    except:
        return "проверьте список учеников!"


def wrap_res(res_schedule: list):
    # функция  для читабельного вывода результата
    return f"Расписание на: {res_schedule[0]}\nВоскресенье: {res_schedule[1]}\nПонедельник:{res_schedule[2]}\nВторник: {res_schedule[3]}\nСреда: {res_schedule[4]}\nЧетверг: {res_schedule[5]}\n"


@dp.message_handler(Text(equals="Назад"))
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Расписание", "Список учеников"]
    keyboard.add(*buttons)
    await message.answer("Что вы хотите?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Расписание"))
async def schedule_actual(message: types.Message):
    '''
    Выдает страое расписание если есть,
    если нет генерирует новое
    '''
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Новое расписание", "Прошлые расписания", "Назад"]
    keyboard.add(*buttons)
    try:
        with open('store_file.yaml') as stream:
            res_schedule = list(yaml.safe_load(stream).values())[-1]
            try:
                await message.answer(wrap_res(res_schedule), reply_markup=keyboard)
            except:
                await message.answer(wrap_res(colel_schedule()), reply_markup=keyboard)
    except:
        await message.answer(wrap_res(colel_schedule()), reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Список учеников")
async def pupil_list(message: types.Message):
    # дает ссылку на таблицу с учениками
    await message.answer(
        'https://docs.google.com/spreadsheets/d/1ljIQbUyL_RMii47joDgWRfXr4q15e4mSw1oA1ZxI8D0/edit#gid=0')


@dp.message_handler(lambda message: message.text == "Новое расписание")
async def new_schedule(message: types.Message):
    # генерирует новое расписание
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Новое расписание", "Прошлые расписания", "Назад"]
    keyboard.add(*buttons)
    await message.answer(wrap_res(colel_schedule()), reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Прошлые расписания")
async def new_schedule(message: types.Message):
    # возращает предыдущие расписания
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Новое расписание", "Прошлые расписания", "Назад"]
    keyboard.add(*buttons)
    try:
        with open('store_file.yaml') as stream:
            res_schedule = list(yaml.safe_load(stream).values())
            for row in res_schedule:
                await message.answer(' '.join(map(str, row)), reply_markup=keyboard)
    except:
        await message.answer("отсутствуют")


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
