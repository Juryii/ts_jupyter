import pandas as pd
from src.utils import get_df_data

class PipeSupport:
    """
    Класс для создания опор трубопроводов по ОСТ 36-146-88.

    Атрибуты:
        dn (float): Наружный диаметр трубы.
        support_type (str): Тип опоры (например, "КП").
        execution (str): Исполнение опоры (например, "А11" или "АС11").
        count (int): Количество опор.
        mass_per_support (float): Масса одной опоры (кг).
        total_mass (float): Общая масса опор (кг).
    """

    def __init__(self, dn, support_type="КП", execution="А11", steel_grade="ВСт3пс", gost_name="ОСТ 36-146-88"):
        """
        Инициализация объекта PipeSupport.

        Параметры:
            dn (float): Наружный диаметр трубы.
            support_type (str): Тип опоры (например, "КП"). Используется для формирования имени файла.
            execution (str): Исполнение опоры (например, "А11").
            steel_grade (str): Марка стали (по умолчанию "ВСт3пс").
            gost_name (str): Название ГОСТа (по умолчанию "ОСТ 36-146-88").

        Исключения:
            ValueError: Если параметры не соответствуют данным ОСТ.
        """
        # Получение данных из ОСТ
        file_name = f"{support_type} {gost_name}"
        df = get_df_data(file_name)

        # Проверка входных данных
        checked_support = self.__check_support(df, dn, execution)

        # Инициализация атрибутов
        self.dn = checked_support['dn']
        self.support_type = support_type
        self.execution = execution
        self.steel_grade = steel_grade
        self.gost_name = gost_name
        self.mass_per_support = float(checked_support['mass'])


    def __str__(self):
        """
        Возвращает строковое представление объекта PipeSupport.

        Формат строки:
        "Опора {Диаметр}-{Тип}-{исполнение}-{сталь} {номер ГОСТа}".
        Например: "Опора 159-КП-А12-ВСт3пс ОСТ 36-146-88".
        """
        return (f"Опора {self.dn}-{self.support_type}-{self.execution}-{self.steel_grade} {self.gost_name}")

    def __repr__(self):
        """
        Возвращает подробное строковое представление объекта PipeSupport.

        Формат строки:
        "Опора типа {Тип} исполнения {Исполнение} из стали {Марка стали} для трубопровода Dн={Диаметр}мм".
        Например: "Опора типа КП исполнения А12 из стали ВСт3пс для трубопровода Dн=159мм".
        """
        return (f"Опора типа {self.support_type} исполнения {self.execution} из стали {self.steel_grade} для трубопровода Dн={self.dn}мм")

    def __check_support(self, df, dn, execution):
        """
        Проверяет наличие комбинации параметров в ОСТ.

        Параметры:
            df (DataFrame): Данные ОСТ.
            dn (float): Наружный диаметр трубы.
            execution (str): Исполнение опоры.

        Возвращает:
            DataFrame: Отфильтрованные данные опоры.

        Исключения:
            ValueError: Если параметры отсутствуют в ОСТ.
        """
        if dn not in df['dn'].values:
            raise ValueError(f"Диаметр {dn} отсутствует в ОСТ 36-146-88.")

        filtered_df = df[df['dn'] == dn].copy()

        if filtered_df.empty:
            raise ValueError(f"Для диаметра {dn} нет данных в ОСТ 36-146-88.")

        # Обработка двойных значений в колонке Execution
        # Значения разделяются по '/' и очищаются от лишних пробелов для удобства сравнения.
        filtered_df['Execution'] = filtered_df['Execution'].apply(lambda x: [item.strip() for item in x.split('/')])
        valid_rows = filtered_df[filtered_df['Execution'].apply(lambda x: execution.strip() in x)]

        if valid_rows.empty:
            available_executions = ', '.join(
                sorted({item.strip() for sublist in filtered_df['Execution'] for item in sublist})
            )
            raise ValueError(
                f"Исполнение {execution} отсутствует для диаметра {dn}. "
                f"Доступные исполнения: {available_executions}.")

        # Преобразование списка обратно в строку для хранения
        valid_row = valid_rows.iloc[0].copy()
        valid_row['Execution'] = '/'.join(valid_row['Execution'])

        return valid_row
