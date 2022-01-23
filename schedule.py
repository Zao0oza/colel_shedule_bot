# создает расписание дежурств на пятидневку
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


