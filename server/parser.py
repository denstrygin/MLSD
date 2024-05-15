import pandas as pd
from search import COLORMAP

CLASSES = [
    "Фон",
    "Гусли",
    "Курительная трубка",
    "Шкатулка",
    "Меч",
    "Шлем",
    "Череп",
    "Череп с венком",
    "Книга",
    "Перевернутый вниз стакан",
    "Часы",
    "Песочные часы",
    "Ключ",
    "Пустой стакан",
    "Саквояж",
    "Потухшая свеча",
    "Морская раковина",
    "Опавший лист",
    "Медецинский инструмент",
    "Мыльный пузырь",
    "Разбитая посуда",
    "Ноты",
    "Нож",
    "Флейта",
    "Кошель",
    "Тюльпан",
    "Роза",
    "Ландыш",
    "Фиалка",
    "Лилия",
    "Гвоздика",
    "Нарцисс",
    "Ирис",
    "Вьюнок",
    "Бабочка",
    "Бокал с вином",
    "Виноград",
    "Вишня",
    "Высокий стеклянный бокал",
    "Гранат, треснутый",
    "Инжир, треснутый",
    "Кубок-наутилоса",
    "Лимон кусочком",
    "Лимон с кожурой",
    "Мясной пирог",
    "Наклоненный/пустой стакан",
    "Оливка",
    "Открытая устрица",
    "Персик, нарезанный",
    "Улитка",
    "Хлеб",
]

async def parse_response(coll, id):
    if id == '-1':
        query = {}
    else:
        query = {'_id': int(id)}

    response = []
    async for document in coll.find(query):
        document.pop('_id', None)

        for key in document.keys():
            subkeys = list(document[key].keys()) if isinstance(document[key], dict) else []
            response.append({"name": key, "symbols": subkeys})

    return response

async def get_semantic(coll, id, classes):
    if id == -1:
        query = {}
    else:
        query = {'_id': id}
    response = []
    cursor = coll.find(query)
    async for i in cursor:
        i.pop('_id', None)
        for j, class_present in enumerate(classes):
            if class_present:
                symbol = CLASSES[j]
                for key in i.keys():
                    skeys = list(i[key].keys())
                    for skey in skeys:
                        if skey == symbol:
                            response.append({
                                "symbol": skey,
                                "semantic": i[key][skey],
                                "color": COLORMAP[j]
                            })
    return response

def kill_NaN(arr):
    for i in range(len(arr)):
        if pd.isna(arr[i]):
            arr[i] = arr[i - 1]

def parserDutchStyleLife():
    try:
        dutchStyleLife = pd.read_excel(r'./dutchStyleLife.xlsx', sheet_name='Лист1')
        breakpoint = -1
        result = {}
        kill_NaN(dutchStyleLife['Значения'])
        for i in range(len(dutchStyleLife['Жанры натюрмортов'])):
            if not(pd.isna(dutchStyleLife['Жанры натюрмортов'][i])):
                key = dutchStyleLife['Жанры натюрмортов'][i]
                if breakpoint != -1:
                    result[dutchStyleLife['Жанры натюрмортов'][breakpoint]] = dict(zip(dutchStyleLife['Сегменты'][breakpoint:i].to_list(), dutchStyleLife['Значения'][breakpoint:i].to_list()))
                breakpoint = i
        else:
            result[key] = dict(zip(dutchStyleLife['Сегменты'][breakpoint:i + 1].to_list(), dutchStyleLife['Значения'][breakpoint:i + 1].to_list()))
        return result
    except: 
        return 'Parser Error'

if __name__ == "__main__":
    print(parserDutchStyleLife())