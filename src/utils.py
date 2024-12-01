# файл с вспомогательными функциями
import pandas as pd
from functools import lru_cache


gost_paths = {
        "ГОСТ 8732-78": "/home/jovyan/work/ts_jupyter/src/data/pipes/gost_8732-78.csv",
        "ГОСТ 8734-75": "/home/jovyan/work/ts_jupyter/src/data/pipes/gost_8734-75.csv",
        "ГОСТ 10704-91": "/home/jovyan/work/ts_jupyter/src/data/pipes/gost_10704-91.csv",

        "ГОСТ 17375-2001": "/home/jovyan/work/ts_jupyter/src/data/elbows/gost_17375-2001.csv",
    }

@lru_cache(maxsize=5)  # Хранить до 5 различных ГОСТов
def get_df_data(gost_name):
            # Проверка наличия ГОСТа в доступных путях
    if gost_name not in gost_paths:
        raise ValueError(f"ГОСТ '{gost_name}' не найден в доступных путях.")
        
    url = gost_paths[gost_name]
    
    df = pd.read_csv(url, sep=";")
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')] # Удаление ошибочных колонок
    df = df.replace(',', '.', regex=True)  # Замена запятой на точку
    df = df.apply(pd.to_numeric, errors='coerce')  # Приведение к числовому типу
    return df