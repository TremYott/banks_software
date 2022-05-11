import datetime
from .Account import Account
from .Account import CreditAccount
from .Account import DebtAccount
from .BankTasks import BankTasks


class Time:

    def __init__(self):
        self.debtrate = 8, 9  # ставка процента вклада
        self.creditrate = 5  # ставка процента кредита
        self.debtdays = 180  # на какое кол-во дней открыт вклад
        self.creditmonths = 12  # на какое кол-во дней открыт кредит
        self.creditmonths_recalc = 2  # кол-во месяцев, через которых мы делаем перерасчет кредита
        self.debtdays_recalc = 5  # кол-во дней, через сколько от начала вклада мы хотим перерасчитать сумму

    @staticmethod
    def now():
        dt_now = datetime.datetime.today()
        return dt_now

    # конечное количество денег на вкладе
    def debt_subscribe(self):
        debt_percent = (DebtAccount().amount * self.debtrate * self.debtdays) / (365 * 100)
        debtsum = DebtAccount().amount + debt_percent
        return debtsum

    # сумма кредита   
    def credit_subscribe(self):
        creditsum = CreditAccount().amount

    # какой будет сумма на вкладе через self.debtdays_recalc дней
    def debt_rewind(self):
        debt_percent = (BankTasks().onDebtDayEnd() * self.debtrate * (self.debtdays - self.debtdays_recalc)) / (
                    365 * 100)
        debtsum = BankTasks().onDebtDayEnd() + debt_percent
        return debtsum

    # сколько останется заплатить по кредиту через self.creditmonths_recalc месяцев
    def cridet_rewind(self):
        creditsum = CreditAccount().amount - Account().calcCreditMonthlyPercent * (
                    self.creditmonths - self.creditmonths_recalc)
        return creditsum
