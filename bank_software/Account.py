from bank_software.bank import Bank
from bank_software.terms import Terms
from bank_software.user import User


class Account:
    def __init__(self, ident, user: User, terms: Terms):
        self.id = ident
        self.user = user
        self.amount = 0
        self.percents_storage = []
        self.terms = terms
        self.sus_status = False

    def check_sus_status(self):
        if self.user.address & self.user.passport:
            self.sus_status = True

    def topUp(self, cash, bank):
        self.amount += bank.Transaction_topUp(cash)
        # self.amount+=cash

    def withdraw(self, cash, bank):
        if self.sus_status or cash < self.terms.restrictions:
            if bank.Transaction_withdraw(cash) > self.amount:
                print("Ошибка. Недостаточно средств")
            else:
                self.amount -= bank.Transaction_withdraw(cash)
        else:
            print("Ошибка. Заполните свои паспортные данные и/или адрес")

    def calcDailyPercent(self, bankTasks):
        self.percents_storage.append(bankTasks.onDayEnd * self.terms.percent / 100)

    def calcMonthlyPercent(self):
        self.amount += sum(self.percents_storage)
        self.percents_storage = []


class DebtAccount(Account):
    pass


class DepositAccount(Account):
    def __init__(self, ident, amount, duration, user: User, terms: Terms):
        super().__init__(ident, user, terms)
        self.amount = amount
        self.duration = duration
        self.open_time = Time.now()
        self.percents_storage = []
        if amount <= 50000:
            self.percents = 3
        elif amount <= 100000:
            self.percents = 3.5
        else:
            self.percents = 4

    def withdraw(self, cash, bank: Bank):
        if Time.now() - self.duration >= open_time:
            if bank.Transaction_withdraw(cash) > self.amount:
                print("Ошибка. Недостаточно средств.")
            else:
                self.amount -= bank.Transaction_withdraw(cash)
        else:
            print("Ошибка. Окончание времени депозита не наступило.")


class CreditAccount(Account):
    def __init__(self, ident, limit, credit_cash, terms: Terms, user: User):
        super().__init__(ident, user, terms)
        self.limit = limit  # должен быть отрицательным
        self.status = False

    def withdraw_comission(self, bank: Bank):
        if self.status:
            self.amount -= bank.Transaction_withdraw(self.terms.commission)

    def withdraw(self, cash, bank: Bank):
        if self.amount - bank.Transaction_withdraw(cash) < self.limit:
            print("Ошибка. Превышен лимит")
        elif self.amount - bank.Transaction_withdraw(cash) < 0:
            self.amount -= bank.Transaction_withdraw(cash)
            self.status = True
