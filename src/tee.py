import pandas as pd
from src.utils import get_df_data

class PipeTee():
    """
    Класс для создания тройников трубопроводов.

    Атрибуты:
        tee_dn1 (float): Наружный диаметр магистрали тройника.
        tee_thicknes1 (float): Толщина стенки магистрали.
        tee_dn2 (float): Наружный диаметр ответвления тройника.
        tee_thicknes2 (float): Толщина стенки ответвления.
        tee_count (int): Количество тройников.
        steel_grade (str): Марка стали.
        gost_name (str): Название ГОСТа.
        nominal_diameter (float): Номинальный диаметр магистрали.
        tee_type (int): Исполнение тройника.
        mass_per_tee (float): Масса одного тройника (кг).
        total_mass (float): Общая масса тройников (кг).
    """
    def __init__(self, tee_dn1, tee_thicknes1, tee_dn2, tee_thicknes2, tee_count, steel_grade="Сталь 20", gost_name="ГОСТ 17376-2001"):
        """
        Инициализирует объект PipeTee.

        Проверяет входные параметры и инициализирует атрибуты объекта.

        Параметры:
            tee_dn1 (float): Наружный диаметр магистрали тройника.
            tee_thicknes1 (float): Толщина стенки магистрали.
            tee_dn2 (float): Наружный диаметр ответвления тройника.
            tee_thicknes2 (float): Толщина стенки ответвления.
            tee_count (int): Количество тройников.
            steel_grade (str): Марка стали (по умолчанию "Сталь 20").
            gost_name (str): Название ГОСТа (по умолчанию "ГОСТ 17376-2001").

        Исключения:
            ValueError: Если входные параметры не соответствуют данным ГОСТ.
        """
        # получение данных из ГОСТа
        df = get_df_data(gost_name)
        # проверка входных данных на соответствие с данными в ГОСТе
        checked_tee = self.__check_tee(df, tee_dn1, tee_thicknes1, tee_dn2, tee_thicknes2, gost_name)
        
        # Инициализация атрибутов   
        
        # Определение номинального диаметра (DN) по наружному диаметру
        self.nominal_diameter = df[df['D'] == tee_dn1]['DN'].values[0]
        
        self.tee_dn1 = checked_tee['D'].values[0]  # Наружный диаметр магистрали        
        self.tee_thicknes1 = checked_tee['T'].values[0]  # Толщина стенки магистрали
        self.tee_dn2 = checked_tee['D1'].values[0]   # Наружный диаметр ответвления
        self.tee_thicknes2 = checked_tee['T1'].values[0]  # Толщина стенки магистрали
        self.tee_count = tee_count
        self.steel_grade = steel_grade
        self.gost_name = gost_name
        self.tee_type = checked_tee['Execution'].values[0]  # Исполнение тройника, колнка execution
        self.mass_per_tee = checked_tee['mass'].values[0]  # масса одного тройника
        self.total_mass = round(self.tee_count * self.mass_per_tee) # общая масса тройников
        

    def __str__(self):
        """
        Возвращает строковое представление объекта PipeTee.

        Формат строки:
        - Для одинаковых диаметров магистрали и ответвления: "Тройник {тип}-{диаметр}х{толщина} ГОСТ".
        - Для разных диаметров: "Тройник {тип}-{магистраль}х{толщина магистрали}-{ответвление}х{толщина ответвления} ГОСТ".
        """
        tee_type_str = f"{self.tee_type}-" if self.tee_type != 2 else ""
        steel_grade_str = f"-{self.steel_grade}" if self.steel_grade != "Сталь 20" else ""
        if self.tee_dn1 == self.tee_dn2:
            return f"Тройник {tee_type_str}{self.tee_dn1}х{self.tee_thicknes1}{steel_grade_str} {self.gost_name}"
        else:
            return f"Тройник {tee_type_str}{self.tee_dn1}х{self.tee_thicknes1}-{self.tee_dn2}х{self.tee_thicknes2}{steel_grade_str} {self.gost_name}"

    def __repr__(self):
        """
        Возвращает подробное строковое представление объекта PipeTee.

        Формат:
        "Тройник {тип}-{магистраль}х{ответвление} (DN {номинальный диаметр}) {ГОСТ}, масса: {масса одного}, общая масса: {общая масса}".
        """
        steel_grade_str = f"-{self.steel_grade}" if self.steel_grade != "Сталь 20" else ""
        return (
            f"Тройник {self.tee_type}-{self.tee_dn1}х{self.tee_dn2} "
            f"(DN {self.nominal_diameter}){steel_grade_str} "
            f"{self.gost_name}, масса одного тройника: {self.mass_per_tee} кг, "
            f"общая масса: {self.total_mass} кг"
        )

    def __check_tee(self, df, tee_dn1, tee_thicknes1, tee_dn2, tee_thicknes2, gost_name):
        """
        Проверяет наличие комбинации параметров в ГОСТ.

        Параметры:
            df (DataFrame): Данные ГОСТ.
            tee_dn1 (float): Наружный диаметр магистрали.
            tee_thicknes1 (float): Толщина стенки магистрали.
            tee_dn2 (float): Наружный диаметр ответвления.
            tee_thicknes2 (float): Толщина стенки ответвления.
            gost_name (str): Название ГОСТ.

        Возвращает:
            DataFrame: Отфильтрованные данные тройника.

        Исключения:
            ValueError: Если параметры отсутствуют в ГОСТ.
        """
        
        # Проверка наличия диаметра магистрали
        if tee_dn1 not in df['D'].values:
            raise ValueError(
                f"Диаметр {tee_dn1} отсутствует в {gost_name}."
            )
    
        # Проверка наличия толщины стенки магистрали
        if tee_thicknes1 not in df[df['D'] == tee_dn1]['T'].values:
            available_thicknesses1 = df[df['D'] == tee_dn1]['T'].dropna().unique()
            raise ValueError(
                f"Толщина стенки {tee_thicknes1} для магистрали {tee_dn1} отсутствует в {gost_name}. "
                f"Доступные толщины: {', '.join(map(str, available_thicknesses1))}."
            )
    
        # Проверка наличия диаметра ответвления
        if tee_dn2 not in df['D1'].values:
            raise ValueError(
                f"Диаметр {tee_dn2} отсутствует в {gost_name}."
            )
    
        # Проверка наличия толщины стенки ответвления
        if tee_thicknes2 not in df[df['D1'] == tee_dn2]['T1'].values:
            available_thicknesses2 = df[df['D1'] == tee_dn2]['T1'].dropna().unique()
            raise ValueError(
                f"Толщина стенки {tee_thicknes2} для ответвления {tee_dn2} отсутствует в {gost_name}. "
                f"Доступные толщины: {', '.join(map(str, available_thicknesses2))}."
            )
    
        # Проверка наличия полной комбинации параметров
        df_tee = df[
            (df['D'] == tee_dn1) &
            (df['T'] == tee_thicknes1) &
            (df['D1'] == tee_dn2) &
            (df['T1'] == tee_thicknes2)
        ]
        if df_tee.empty:
            combinations = self.get_available_thickness_combinations(df, tee_dn1, tee_dn2)
            formatted_combinations = ", ".join([f"({t}, {t1})" for t, t1 in combinations])

            raise ValueError(
                f"Комбинация параметров (D={tee_dn1}, T={tee_thicknes1}, D1={tee_dn2}, T1={tee_thicknes2}) "
                f"отсутствует в ГОСТ {gost_name}. \n"
                f"Проопробуйте следующие комбинации толщин стенок: {formatted_combinations}."
            )
    
        return df_tee

    def get_available_thickness_combinations(self, df, tee_dn1, tee_dn2):
        """
        Возвращает доступные комбинации толщин стенок для заданных диаметров магистрали и ответвления.
    
        Параметры:
            df (DataFrame): DataFrame с данными о тройниках.
            tee_dn1 (float): Наружный диаметр магистрали тройника.
            tee_dn2 (float): Наружный диаметр ответвления тройника.
    
        Возвращает:
            List[Tuple[float, float]]: Список доступных комбинаций (толщина магистрали, толщина ответвления).
        """
        # Фильтрация DataFrame по диаметрам
        filtered_df = df[(df['D'] == tee_dn1) & (df['D1'] == tee_dn2)]
    
        # Извлечение уникальных комбинаций толщин стенок
        available_combinations = filtered_df[['T', 'T1']].dropna().drop_duplicates()
    
        # Преобразование в список кортежей
        return list(available_combinations.itertuples(index=False, name=None))
            