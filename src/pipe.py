import pandas as pd

class Pipe:
    """
    Класс для представления трубы согласно стандартам ГОСТ.

    Атрибуты:
        gost_name (str): Название ГОСТа, которому соответствует труба.
        pipe_dn (float): Внутренний диаметр трубы (дюймы).
        pipe_thickness (float): Толщина стенки трубы (миллиметры).
        pipe_length (float): Длина трубы (метры).
        mass_per_meter (float): Масса одного метра трубы (кг).
        pipe_mass (float): Общая масса трубы (кг).
    """

    __gost_paths = {
        "ГОСТ 8732-78": "/home/jovyan/work/ts_jupyter/src/data/pipes/gost_8732-78.csv",
        "ГОСТ 8734-75": "/home/jovyan/work/ts_jupyter/src/data/pipes/gost_8734-75.csv",
        "ГОСТ 10704-91": "/home/jovyan/work/ts_jupyter/src/data/pipes/gost_10704-91.csv",
    }

    def __init__(self, gost_name, pipe_dn, pipe_thickness, pipe_length):
        """
        Инициализация объекта Pipe.

        Проверяет наличие указанного ГОСТа, загружает данные из соответствующего файла,
        проверяет корректность входных данных и рассчитывает массу трубы.

        Параметры:
            gost_name (str): Название ГОСТа.
            pipe_dn (float): Внутренний диаметр трубы.
            pipe_thickness (float): Толщина стенки трубы.
            pipe_length (float): Длина трубы.
        
        Исключения:
            ValueError: Если указанный ГОСТ не найден или входные параметры некорректны.
        """
        # Проверка наличия ГОСТа в доступных путях
        if gost_name not in self.__gost_paths:
            raise ValueError(f"ГОСТ '{gost_name}' не найден в доступных путях.")
        
        # Загрузка данных о трубах из CSV файла
        relative_path = self.__gost_paths[gost_name]
        df = pd.read_csv(relative_path, sep=";")
        df = df.replace(',', '.', regex=True)  # Замена запятой на точку
        df = df.apply(pd.to_numeric, errors='coerce')  # Приведение к числовому типу

        # Проверка корректности параметров трубы
        self.__check_pipe(df, pipe_dn, pipe_thickness)

        # Инициализация атрибутов
        self.gost_name = gost_name
        self.pipe_length = pipe_length
        self.pipe_dn = pipe_dn
        self.pipe_thickness = pipe_thickness
        
        # Получение массы одного метра трубы из DataFrame
        self.mass_per_meter = float(df[df['dn'] == pipe_dn].dropna(axis=1, how='all')[str(pipe_thickness).replace('.', ',')].values[0])
        
        # Расчет общей массы трубы
        self.pipe_mass = round(self.pipe_length * self.mass_per_meter, 2)

    def install_pipe(self, length_0_8m, length_8_10m, length_over_10m):
        """
        Монтаж трубы на высоте.

        :param length_0_8m: Длина установки трубы на высоте от 0 до 8м.
        :param length_8_10m: Длина установки трубы на высоте от 8 до 10м.
        :param length_over_10m: Длина установки трубы на высоте свыше 10м.
        :raises ValueError: Если общая длина установки превышает общую длину трубы.
        :return: True, если установка прошла успешно.
        """
        total_installation_length = length_0_8m + length_8_10m + length_over_10m
        
        if total_installation_length > self.pipe_length:
            raise ValueError(f"Общая длина установки {total_installation_length}м превышает длину трубы {self.pipe_length}м.")
        
        self.height_installation_0_8m = length_0_8m
        self.height_installation_8_10m = length_8_10m
        self.height_installation_over_10m = length_over_10m
        return True
    
    def __check_pipe(self, df, pipe_dn, pipe_thickness):
        """
        Проверяет корректность параметров трубы.

        Параметры:
            df (DataFrame): DataFrame с данными о трубах.
            pipe_dn (float): Внутренний диаметр трубы.
            pipe_thickness (float): Толщина стенки трубы.

        Исключения:
            ValueError: Если входные параметры некорректны.
        """
        # Проверка наличия столбца 'dn' в DataFrame
        if 'dn' not in df.columns:
            raise ValueError("Столбец 'dn' не найден в файле.")
        
        # Проверка наличия внутреннего диаметра в DataFrame
        if pipe_dn not in df['dn'].values:
            raise ValueError(f"Значение {pipe_dn} отсутствует в столбце 'dn'.")

        # Извлечение данных о толщине стенки для указанного диаметра
        pipe_thickness_df = df[df['dn'] == pipe_dn].dropna(axis=1, how='all')
        all_columns = pipe_thickness_df.columns.astype(str)
        columns_without_dn = [col for col in all_columns if col != 'dn']
        
        # Преобразование толщины стенки в строку
        pipe_thickness_str = str(pipe_thickness).replace('.', ',')
        
        # Проверка наличия толщины стенки в доступных колонках
        if pipe_thickness_str not in columns_without_dn:
            error_message = (
                f"Ошибка: Данная толщина стенки '{pipe_thickness_str}' отсутствует для диаметра '{pipe_dn}'.\n"
                f"Допустимый список толщин: {', '.join(columns_without_dn)}"
            )
            raise ValueError(error_message)

    def __str__(self):
        """
        Возвращает строковое представление объекта Pipe.

        Возвращает информацию о трубе, включая ГОСТ, размеры, длину и массу.
        
        Возвращаемое значение:
            str: Строка с информацией о трубе.
        """
        return f"Труба {self.gost_name} {self.pipe_dn}х{self.pipe_thickness} длиной {self.pipe_length}м, масса 1м трубы {self.mass_per_meter} кг, масса всей трубы: {self.pipe_mass}"



# Пример использования
#pipe_instance = Pipe("ГОСТ 8732-78", 57, 3.5, 10)

