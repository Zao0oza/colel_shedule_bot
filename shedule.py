# создает расписание дежурств на пятидневку
pupildict = {'John': 1, 'Peter': 1, 'Vova': 1, 'Zalman': 0, 'Igor': 0, 'Lena': 1, 'Baruh': 0, 'Inna': 1}
pupildict2 = {'John': 1, 'Peter': 1, 'Vova': 1}
sched = list(pupildict.keys())


def colel_schedule(pupildict: dict):
    i = 0
    """
    Получаем словарь со списком людей отсортированный по количеству дежурств
    """
    sortedpupils = dict(sorted(pupildict.items(), key=lambda x: x[1]))
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
    """
    for i in pupilres:
        pupildict[i] += 1
    print(pupildict)
    return pupilres


print(colel_schedule(pupildict))
print(colel_schedule(pupildict))
print(colel_schedule(pupildict))
print(colel_schedule(pupildict))
print(colel_schedule(pupildict))
print(colel_schedule(pupildict))
