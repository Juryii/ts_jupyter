import pandas as pd
from src.utils import get_df_data


class PipeElbow:
    """
    Класс для создания отводов трубопроводов.
    """

    def __init__(self, elbow_dn, elbow_thickness, elbow_angle, elbow_count, steel_grade="Сталь 20", gost_name="ГОСТ 17375-2001"):
        """
        Инициализация объекта PipeElbow.

        Параметры:
            elbow_dn (float): Наружный диаметр отвода.
            elbow_thickness (float): Толщина стенки отвода.
            elbow_angle (int): Угол отвода (например, 45, 90).
            elbow_count (int): Количество отводов.
            steel_grade (str): Марка стали (по умолчанию "Сталь 20").
            gost_name (str): Название ГОСТа (по умолчанию "ГОСТ 17375-2001").
        """
        # Загрузка данных об отводах из CSV файла
        df = get_df_data(gost_name)
        df = df.apply(pd.to_numeric, errors='coerce')  # Приведение к числовому типу

        # Проверка корректности параметров отвода
        self.__check_elbow(df, elbow_dn, elbow_thickness, elbow_angle, gost_name)

        # Инициализация атрибутов
        self.gost_name = gost_name
        self.elbow_dn = elbow_dn  # Наружный диаметр
        self.elbow_thickness = elbow_thickness
        self.elbow_angle = elbow_angle
        self.elbow_count = elbow_count
        self.steel_grade = steel_grade

        # Определение номинального диаметра (DN) по наружному диаметру
        self.nominal_diameter = float(df[df['D'] == elbow_dn]['DN'].values[0])

        # Определение типа отвода
        self.elbow_type = 1 if elbow_angle <= 90 else 2

        # Расчёт массы одного отвода
        self.mass_per_elbow = float(
            df[
                (df['D'] == elbow_dn) & (df['T'] == elbow_thickness)
            ][f'Mass_{elbow_angle}'].values[0]
        )

        # Общая масса отводов
        self.total_mass = round(self.elbow_count * self.mass_per_elbow, 2)

    def __str__(self):
        """
        Возвращает строковое представление объекта PipeElbow.
        """
        
        if self.steel_grade != "Сталь 20":
            steel_grade_str = f"-{self.steel_grade}"
        else:
            steel_grade_str = ""

        
        if self.elbow_type == 1:
            return f"Отвод {self.elbow_angle}-{self.elbow_type}-{self.elbow_dn}х{self.elbow_thickness}{steel_grade_str} {self.gost_name}"
        else:
            return f"Отвод {self.elbow_angle}-{self.elbow_dn}х{self.elbow_thickness}{steel_grade_str} {self.gost_name}"

    def __check_elbow(self, df, elbow_dn, elbow_thickness, elbow_angle, gost_name):
        """
        Проверяет корректность параметров отвода.

        Параметры:
            df (DataFrame): DataFrame с данными об отводах.
            elbow_dn (float): Наружный диаметр отвода.
            elbow_thickness (float): Толщина стенки отвода.
            elbow_angle (int): Угол отвода.

        Исключения:
            ValueError: Если параметры некорректны.
        """
        # Проверка наличия наружного диаметра (D) в данных
        if elbow_dn not in df['D'].values:
            raise ValueError(f"Наружный диаметр {elbow_dn} отсутствует в {gost_name}.")

        # Проверка толщины стенки
        available_thicknesses = df[df['D'] == elbow_dn]['T'].dropna().unique()
        if elbow_thickness not in available_thicknesses:
            raise ValueError(
                f"Толщина стенки {elbow_thickness} отсутствует для наружного диаметра {elbow_dn}. "
                f"Доступные толщины: {', '.join(map(str, available_thicknesses))}"
            )

        # # Проверка толщины стенки
        # if elbow_thickness not in df[df['D'] == elbow_dn]['T'].values:
        #     raise ValueError(
        #         f"Толщина стенки {elbow_thickness} отсутствует для наружного диаметра {elbow_dn}."
        #     )

        # Проверка угла отвода
        valid_angles = [45, 60, 90, 180]
        if elbow_angle not in valid_angles:
            raise ValueError(
                f"Угол {elbow_angle} не поддерживается. Допустимые углы: {valid_angles}."
            )

    def __repr__(self):
        """
        Возвращает строковое представление объекта PipeElbow.
        """
        steel_grade_str = f"-{self.steel_grade}" if self.steel_grade != "Сталь 20" else ""
        return (
            f"Отвод {self.elbow_angle}-{self.elbow_type}-"
            f"{self.elbow_dn}х{self.elbow_thickness} "
            f"(DN {self.nominal_diameter}){steel_grade_str} "
            f"{self.gost_name}, масса одного отвода: {self.mass_per_elbow} кг, "
            f"общая масса: {self.total_mass} кг"
        )
