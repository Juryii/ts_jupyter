# файл с вспомогательными функциями
import os
import sys
import pandas as pd
from functools import lru_cache
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
	sys.path.append(module_path)

gost_paths = {
        "ГОСТ 8732-78": "/src/data/pipes/gost_8732-78.csv", # трубы стальные бесшовные горячедеформированные
        "ГОСТ 8734-75": "/src/data/pipes/gost_8734-75.csv", # трубы стальные бесшовные холоднодеформированные
        "ГОСТ 10704-91": "/src/data/pipes/gost_10704-91.csv", # трубы стальные электросварные прямошовные

        "ГОСТ 17375-2001": "/src/data/elbows/gost_17375-2001.csv", # отводы
        "ГОСТ 17376-2001": "/src/data/tees/gost_17376-2001.csv", # тройники

        "ГОСТ 17378-2001": "/src/data/transitions/gost_17378-2001.csv", # переходы

        "КП ОСТ 36-146-88": "/src/data/supports/KP_OST_36-146-88.csv" # опоры  КП
    }

@lru_cache(maxsize=5)  # Хранить до 5 различных ГОСТов
def get_df_data(gost_name: str) -> pd.DataFrame:
    """
    Загружает данные из CSV файла для указанного ГОСТа.

    Параметры:
    -----------
    gost_name : str
        Название ГОСТа, например: "ГОСТ 8732-78", "ГОСТ 8734-75", "ГОСТ 10704-91".

    Возвращает:
    -----------
    pd.DataFrame
        Данные в формате DataFrame, очищенные от ненужных колонок и приведенные к числовому формату.

    Исключения:
    -----------
    ValueError
        Если ГОСТ отсутствует в словаре gost_paths.
    """
    # Проверка наличия ГОСТа в доступных путях
    if gost_name not in gost_paths:
        raise ValueError(f"ГОСТ '{gost_name}' не найден в доступных путях.")

    url = module_path + gost_paths[gost_name]

    df = pd.read_csv(url, sep=";")
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')] # Удаление ошибочных колонок
    df = df.replace(',', '.', regex=True)  # Замена запятой на точку
    #df = df.apply(pd.to_numeric, errors='coerce')  # Приведение к числовому типу
    return df