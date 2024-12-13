import pandas as pd
from src.utils import get_df_data

class PipeTransition:
    """
    Класс для создания переходов трубопроводов.

    Атрибуты:
        dn1 (float): Больший наружный диаметр перехода.
        thickness1 (float): Толщина стенки для большего диаметра.
        dn2 (float): Меньший наружный диаметр перехода.
        thickness2 (float): Толщина стенки для меньшего диаметра.
        count (int): Количество переходов.
        steel_grade (str): Марка стали.
        gost_name (str): Название ГОСТа.
        nominal_diameter (float): Номинальный диаметр магистрали.
        mass_per_transition (float): Масса одного перехода (кг).
        total_mass (float): Общая масса переходов (кг).
    """
    def __init__(self, dn1, thickness1, dn2, thickness2, count, steel_grade="Сталь 20", gost_name="ГОСТ 17378-2001"):
        """
        Инициализирует объект PipeTransition.

        Параметры:
            dn1 (float): Больший наружный диаметр перехода.
            thickness1 (float): Толщина стенки для большего диаметра.
            dn2 (float): Меньший наружный диаметр перехода.
            thickness2 (float): Толщина стенки для меньшего диаметра.
            count (int): Количество переходов.
            steel_grade (str): Марка стали (по умолчанию "Сталь 20").
            gost_name (str): Название ГОСТа (по умолчанию "ГОСТ 17378-2001").

        Исключения:
            ValueError: Если входные параметры не соответствуют данным ГОСТ.
        """
        # Получение данных из ГОСТа
        df = get_df_data(gost_name)

        # Проверка входных данных на соответствие с ГОСТом
        checked_transition = self.__check_transition(df, dn1, thickness1, dn2, thickness2, gost_name)

        # Инициализация атрибутов
        self.nominal_diameter = df[df['D'] == dn1]['DN'].values[0]
        self.dn1 = checked_transition['D'].values[0]
        self.thickness1 = checked_transition['T'].values[0]
        self.dn2 = checked_transition['D1'].values[0]
        self.thickness2 = checked_transition['T1'].values[0]
        self.count = count
        self.steel_grade = steel_grade
        self.gost_name = gost_name
        self.mass_per_transition = checked_transition['mass'].values[0]
        self.total_mass = round(self.count * self.mass_per_transition)

    def __str__(self):
        """
        Возвращает строковое представление объекта PipeTransition.

        Формат строки:
        "Переход {Больший диаметр}х{Меньший диаметр} ГОСТ".
        """
        steel_grade_str = f"-{self.steel_grade}" if self.steel_grade != "Сталь 20" else ""
        return f"Переход {self.dn1}х{self.dn2}{steel_grade_str} {self.gost_name}"

    def __repr__(self):
        """
        Возвращает подробное строковое представление объекта PipeTransition.

        Формат:
        "Переход {Больший диаметр}х{Меньший диаметр} (DN {номинальный диаметр}) {ГОСТ}, масса: {масса одного}, общая масса: {общая масса}".
        """
        steel_grade_str = f"-{self.steel_grade}" if self.steel_grade != "Сталь 20" else ""
        return (
            f"Переход {self.dn1}х{self.dn2} "
            f"(DN {self.nominal_diameter}){steel_grade_str} "
            f"{self.gost_name}, масса одного перехода: {self.mass_per_transition} кг, "
            f"общая масса: {self.total_mass} кг"
        )

    def __check_transition(self, df, dn1, thickness1, dn2, thickness2, gost_name):
        """
        Проверяет наличие комбинации параметров в ГОСТ.

        Параметры:
            df (DataFrame): Данные ГОСТ.
            dn1 (float): Больший наружный диаметр перехода.
            thickness1 (float): Толщина стенки для большего диаметра.
            dn2 (float): Меньший наружный диаметр перехода.
            thickness2 (float): Толщина стенки для меньшего диаметра.
            gost_name (str): Название ГОСТ.

        Возвращает:
            DataFrame: Отфильтрованные данные перехода.

        Исключения:
            ValueError: Если параметры отсутствуют в ГОСТ.
        """
        if dn1 not in df['D'].values:
            raise ValueError(f"Диаметр {dn1} отсутствует в {gost_name}.")

        if thickness1 not in df[df['D'] == dn1]['T'].values:
            available_thicknesses1 = df[df['D'] == dn1]['T'].dropna().unique()
            raise ValueError(
                f"Толщина стенки {thickness1} для магистрали {dn1} отсутствует в {gost_name}. "
                f"Доступные толщины: {', '.join(map(str, available_thicknesses1))}."
            )

        if dn2 not in df['D1'].values:
            available_diameters2 = df[df['D'] == dn1]['D1'].dropna().unique()
            raise ValueError(
                f"Диаметр {dn2} отсутствует в {gost_name}. "
                f"Доступные диаметры для D={dn1}: {', '.join(map(str, available_diameters2))}."
            )

        if thickness2 not in df[df['D1'] == dn2]['T1'].values:
            available_thicknesses2 = df[df['D1'] == dn2]['T1'].dropna().unique()
            raise ValueError(
                f"Толщина стенки {thickness2} для ответвления {dn2} отсутствует в {gost_name}. "
                f"Доступные толщины: {', '.join(map(str, available_thicknesses2))}."
            )

        df_transition = df[
            (df['D'] == dn1) &
            (df['T'] == thickness1) &
            (df['D1'] == dn2) &
            (df['T1'] == thickness2)
        ]

        if df_transition.empty:
            available_combinations = df[(df['D'] == dn1) & (df['D1'] == dn2)][['T', 'T1']].dropna().drop_duplicates()
            available_combinations_str = ', '.join(
                [f"(T={row['T']}, T1={row['T1']})" for _, row in available_combinations.iterrows()]
            )
            raise ValueError(
                f"Комбинация параметров (D={dn1}, T={thickness1}, D1={dn2}, T1={thickness2}) "
                f"отсутствует в ГОСТ {gost_name}. Доступные комбинации толщин: {available_combinations_str}."
            )

        return df_transition
