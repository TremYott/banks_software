import dataclasses


@dataclasses.dataclass
class Terms:
    # Процент на остаток
    percent: int
    # Комиссия за использование, в процентах
    commission: int
    restrictions: any  # этого не было на схеме
