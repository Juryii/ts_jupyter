import pandas as pd
from src.utils import get_df_data

class Armature:
    def __init__(
        self,
        dn,
        pn,
        armature_type,
        flange_count,
        gasket_count,
        additional_gaskets=0,
        rotary_plug=True,
        t1=150,  # Максимальная рабочая температура
        t2=70,   # Минимальная рабочая температура
        t_r=150  # Расчетная температура
    ):
        """
        Конструктор для создания объекта арматуры.

        :param dn: Диаметр номинальный (мм), например, DN 25 мм
        :param pn: Давление номинальное (МПа), например, PN 1,6 МПа
        :param armature_type: Тип арматуры (строка, например, '31с41нж')
        :param flange_count: Количество ответных фланцев, например, 2
        :param gasket_count: Количество основных прокладок, например, 2
        :param additional_gaskets: Количество дополнительных прокладок для испытаний (по умолчанию 0)
        :param rotary_plug: Наличие заглушки поворотной (по умолчанию True)
        :param t1: Максимальная рабочая температура (по умолчанию 150°C)
        :param t2: Минимальная рабочая температура (по умолчанию 70°C)
        :param t_r: Расчетная температура (по умолчанию 150°C)
        """
        self.dn = dn  # Диаметр номинальный, используется в маркировке
        self.pn = pn  # Давление номинальное, влияет на класс прочности
        self.armature_type = armature_type  # Тип арматуры (идентификатор модели)
        self.flange_count = flange_count  # Количество фланцев, входит в комплект поставки
        self.gasket_count = gasket_count  # Количество прокладок в комплекте
        self.additional_gaskets = additional_gaskets  # Дополнительные прокладки для испытаний
        self.rotary_plug = rotary_plug  # Заглушка поворотная, включена в описание
        self.t1 = t1  # Верхний температурный предел рабочего режима
        self.t2 = t2  # Нижний температурный предел рабочего режима
        self.t_r = t_r  # Температура для расчета параметров

    def __str__(self):
        """Метод для строкового представления объекта."""
        description = (
            f"Задвижка клиновая фланцевая исполнения В,\n"
            f"DN{self.dn} мм, PN {self.pn} МПа, сталь 20Л\n"
            f"Класс герметичности А, климатическое\n"
            f"исполнение УХЛ1 по ГОСТ 15150-69,\n"
            f"рабочая среда - вода, температура рабочей среды\n"
            f"{self.t2}°C - {self.t1}°C, расчетная температура {self.t_r}°C\n"
            f"в комплекте:\n"
            f"- ответные фланцы {self.dn}-{int(self.pn*10)}-11-1-В-Ст20-IV ГОСТ 33259-2015 - {self.flange_count} шт.\n"
            f"- прокладки спирально-навивные термостойкие СНП-Д-1-1-{self.dn}-{self.pn} ГОСТ Р 52376-2005 - {self.gasket_count} шт.\n"
        )

        # Добавляем информацию о дополнительных прокладках, если они есть
        if self.additional_gaskets > 0:
            description += (
                f"(доп. прокладки в кол-ве {self.additional_gaskets} шт. для проведения испытаний и запуска системы)\n"
            )

        # Добавляем информацию о заглушке, если она включена
        if self.rotary_plug:
            description += (
                f"- заглушка поворотная 1-{self.dn}-4,0 сталь 20 по АТК 26-18-5-93 - 1 шт.\n"
            )

        description += "- крепеж"

        return description

    def __repr__(self):
        return f"Задвижка {self.armature_type} DN{self.dn} PN{self.pn}"

    def __check_armature(self, dn, armature_type):
        pass
