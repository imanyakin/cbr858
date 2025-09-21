import datetime
import enum

from cbr858.utilities import DatetimeInterval

"""
Приложение 2. Таблица 1.
Определение вероятности дефольта на годовом горизонте в зависимости от группы кредитного риск
"""
credit_quality_pd = {
	1 : 0.01,
	2 : 0.02,
	3 : 0.03,
	4 : 0.04,
	5 : 0.05,
	6 : 0.06,
	7 : 0.07,
	8 : 0.012,
	9 : 0.017,
	10 : 0.25,
	11 : 0.50,
	12 : 0.70,
	13 : 1.30,
	14 : 2.10,
	15 : 3.50,
	16 : 5.00,
	17 : 8.00,
	18 : 15.00,
	19 : 24.00,
	20 : 35.00,
	21 : 50.00,
	22 : 50.00,
	23 : 100.00
}

"""
Приложение 2. Таблица 2.
Коэффициент изменения кредитного спреда в зависимости от группы кредитного качества
"""
credit_spread_change = {
    1 : 0.22,
    2 : 0.27,
    3 : 0.27,
    4 : 0.27,
    5 : 0.34,
    6 : 0.34,
    7 : 0.34,
    8 : 0.8,
    9 : 0.8,
    10 : 0.8,
    11 : 1.15,
    12 : 1.15,
    13 : 1.15,
    14 : 1.95,
    15 : 1.95,
    16 : 1.95,
    17 : 1.95,
    18 : 10.64,
    19 : 10.64,
    20 : 10.64,
    21 : 10.64,
    22 : 10.64,
    23 : 10.64,
}


def relative_interest_rate_change_ruble(duration: float) -> dict:
    """
    Приложение 2. Таблица 3.

    Относительное увеличение или уменьшение процентных ставок, если валютой процентной ставки
    является российский рубль

    :param duration: years
    :return: relative rate change (%), format: (increase, decrease)
    """

    if duration < 0.25:
        (increase,decrease) = (62, -38)
    elif duration < 0.5:
        (increase,decrease) =  (59, -35)
    elif duration < 1:
        (increase,decrease) =  (58, -31)
    elif duration < 2:
        (increase,decrease) =  (55,-29)
    elif duration < 3:
        (increase,decrease) =  (54,-28)
    elif duration < 5:
        (increase,decrease) =  (48, -27)
    elif duration < 7:
        (increase,decrease) =  (42, -26)
    elif duration < 10:
        (increase, decrease) = (34,-24)
    elif duration < 20:
        (increase, decrease) = (20,-18)
    elif duration > 30:
        (increase, decrease) = (14,-15)
    else:
        raise ValueError(f"Invalid {duration=} specified.")

    return {"increase":increase, "decrease":decrease}

def relative_interest_rate_change_yuan(duration: float) -> dict:
    """
    Приложение 2. Таблица 4.

    Относительное увеличение или уменьшение процентных ставок, если валютой процентной
    ставки является китайский юань

    :param duration: years
    :return: relative rate change (%), format: (increase, decrease)
    """
    if duration < 0.25:
        (increase,decrease) = (74, -40)
    elif duration < 0.5:
        (increase,decrease) =  (70, -40)
    elif duration < 1:
        (increase,decrease) =  (68, -40)
    elif duration < 3:
        (increase,decrease) =  (44,-27)
    elif duration < 5:
        (increase,decrease) =  (35,-24)
    elif duration < 7:
        (increase,decrease) =  (28, -22)
    elif duration < 10:
        (increase,decrease) =  (25, -21)
    # todo: check - 20 years missing
    elif duration > 30:
        (increase, decrease) = (16,-17)
    else:
        raise ValueError(f"Invalid {duration=} specified.")

    return {"increase":increase, "decrease":decrease}

def relative_interest_rate_change_other(duration: float) -> dict:
    """
    Приложение 2. Таблица 5.

    Относительное увеличение или уменьшение процентных ставок, если валютой процентной
    ставки иная, чем российский рубль и китайский юань

    :param duration: years
    :return: relative rate change (%), format: (increase, decrease)
    """
    if duration < 0.25:
        (increase,decrease) = (526, -97)
    elif duration < 0.5:
        (increase,decrease) =  (250, -74)
    elif duration < 1:
        (increase,decrease) =  (140, -60)
    elif duration < 2:
        (increase,decrease) =  (84,-55)
    elif duration < 3:
        (increase,decrease) =  (81,-49)
    elif duration < 5:
        (increase,decrease) =  (70, -41)
    elif duration < 7:
        (increase,decrease) =  (58, -35)
    elif duration > 10:
        (increase, decrease) = (42,-30)
    elif duration > 20:
        (increase, decrease) = (29, -30)
    elif duration > 30:
        (increase, decrease) = (24, -27)
    else:
        raise ValueError(f"Invalid {duration=} specified.")
    return {"increase":increase, "decrease": decrease}

def share_price_change(date: datetime.date, coefficient : int ) -> dict:
    """
    Приложение 2. Таблица 6.

    Коэффициент увеличения (снижения) стоимости акций

    :param date: calculation date
    :param coefficient
    :return: share price change dictionary
    """

    assert coefficient in [1,2,3], "Coefficient must be one of [1,2,3]"

    if date < datetime.date(year=2025,month= 12,day=31):
        raise ValueError("Specified date prior to publication of 858-P (17.06.2025)")

    if date <= datetime.date(year=2025,month= 12,day=31):
        price_change = {
            "increase": {1:  18, 2:  25, 3:  25},
            "decrease": {1: -18, 2: -25, 3: -25}
        }
    elif date <= datetime.date(year=2026,month= 12,day=31):
        price_change = {
            "increase": {1:  18, 2:  25, 3:  35},
            "decrease": {1: -18, 2: -25, 3: -35}
        }

    elif date >= datetime.date(year=2027,month= 1,day=1):
        price_change = {
            "increase": {1:  18, 2:  25, 3:  35},
            "decrease": {1: -18, 2: -25, 3: -35}
        }
    else:
        raise ValueError(f"Invalid input date: {date}")

    return {
        "increase": price_change["increase"][coefficient],
        "decrease": price_change["decrease"][coefficient]
    }



"""
Приложение 2. Таблица 7.
Коэффициент изменения курса иностранной валюты по отношению к российскому рублю
"""
currency_change_coefficient_percent = {
    "increase" : 44,  # коэффициент роста (up) курса, relative change (%)
    "decrease" : -9   # коэффициент снижения (down) курса, relative change (%)
}

"""
Приложение 2. Таблица 8.
Коэффициент изменения курса иностранной валюты по отношению к российскому рублю
"""
house_price_coefficient_percent = {
    1 : 10,  # коэффициент 1 снижение стоимости жилой недвижимости, relative change (%)
    2 : 25   # коэффициент 2 снижение стоимости нежилой недвижимости, relative change (%)
}

"""
Приложение 2. Таблица 9.
Коэффициенты увеличения (снижения) стоимости активов, риск изменения стоимости которых не 
подлежит определению в рамках оценки влияния рисков, указанных в абзацак шесом - восьмом, 
десятом подпункта 6.5.1 в 858-П
"""
share_price_unaffected_651 = {
    1 : {"increase": 18, "decrease":-18},
    2: {"increase": 50, "decrease": -50}
}

def concentration_coefficient(date : datetime.date):
    """
    Приложение 2. Таблица 10.
    Коэффициент концентрации (СТ)

    :param date: период
    :return: значение
    """

    if date in DatetimeInterval(start=datetime.date(year=2025, month=9, day=1),
                                end=  datetime.date(year=2026, month=6, day=30)):
        return 9
    elif date in DatetimeInterval(start= datetime.date(year=2026, month=7, day=1),
                                  end =  datetime.date(year=2027, month=6, day=30)
                                  ):
        return 8
    elif date in DatetimeInterval(start= datetime.date(year=2027, month=7, day=1),
                                  end =  datetime.date(year=2028, month=6, day=30)):
        return 7
    elif date in DatetimeInterval(start= datetime.date(year=2028, month=7, day=1),
                                  end=   datetime.date(year=2029, month=6, day=30)):
        return 6
    elif date in DatetimeInterval(start=datetime.date(year=2029, month=7, day=1)):
        return 5
    else:
        raise ValueError(f"Invalid {date=}.")

"""
Приложение 2. Таблица 11.
Предельный срок для определения задолженности перед страховщиков страховых агентов и страховых
(перестраховочных) брокеров
"""
working_days_limit = 20


"""
Приложение 2. Таблица 12.
Коэффициент риска 2 (Q)
"""
risk2_Q = 90

def risk_1_2_correlation_matrix(i,j):
    """
    Приложение 2. Таблица 13.
    Коэффициент корреляции рисков 1 и 2
    """
    assert i in [1,2]
    assert j in [1, 2]

    correlation_matrix = [
        [1, 0.25],
        [0.25, 1],
    ]
    return correlation_matrix[i-1][j-1]

class RiskTypes(enum.Enum):
    concentration = 0
    credit_spread = 1
    interest_rate = 2
    share_price = 3
    currency_exchange = 4
    house_price = 5
    other_assets = 6

def risk_type_correlation_matrix(i : RiskTypes, j : RiskTypes):
    """
    Приложение 2. Таблица 14.
    Коэффициент видов риска 1
    """
    correlation_matrix = [
        [1, 0,    0, 0,    0, 0, 0],
        [0, 1,    1, 1,    1, 1, 1],
        [0, 1,    1, 1, 0.75, 1, 1],
        [0, 1,    1, 1,    1, 1, 1],
        [0, 1, 0.75, 1,    1, 1, 1],
        [0, 1,    1, 1,    1, 1, 1],
        [0, 1,    1, 1,    1, 1, 1],
    ]
    return correlation_matrix[i.value][j.value]

def risk_2_correlation_matrix(i, j):
    """
    Приложение 2. Таблица 15.
    Kоэффициенты корреляции риска 2 между категориями контрагентов

    i : first counterparty category
    j : second counterparty category
    """
    assert i in [1,2,3,4,5]
    assert j in [1, 2, 3, 4, 5]

    correlation_matrix = [
        [1,    0.75, 0.75, 0.25, 0.25],
        [0.75,    1,    1, 0.25, 0.25],
        [0.75,    1,    1, 0.25, 0.25],
        [0.25, 0.25, 0.25,    1,    1]
    ]
    return correlation_matrix[i-1][j-1]

"""
Приложение 2. Таблица 16.
Значене коэффициента z
"""
z_coefficient = {1 : 2, 2 : 1}

