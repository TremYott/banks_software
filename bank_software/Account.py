from bank_software.Time import Time
from bank_software.bank import Bank
from bank_software.terms import Terms
from bank_software.transaction import Transaction
from bank_software.user import User


class Account:
    def __init__(self, ident, bank: Bank, user: User, terms: Terms):
        self.id = ident
        self.user = user
        self.amount = 0
        self.percents_storage = []
        self.terms = terms
        self.sus_status = False
        self.bank = bank

    def check_sus_status(self):
        if self.user.address & self.user.passport:
            self.sus_status = True

    def topUp(self, cash):
        self.amount += self.bank.Transaction_topUp(cash)
        # self.amount+=cash

    def withdraw(self, cash):
        if self.sus_status or cash < self.terms.restrictions:
            if self.bank.withdraw_transaction(cash) > self.amount:
                print("Ошибка. Недостаточно средств")
            else:
                self.amount -= self.bank.withdraw_transaction(cash)
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
    def __init__(self, ident, bank: Bank, amount, duration, user: User, terms: Terms):
        super().__init__(ident, bank, user, terms)
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

    def withdraw(self, cash):
        if Time.now() - self.duration >= open_time:
            if self.bank.withdraw_transaction(cash) > self.amount:
                print("Ошибка. Недостаточно средств.")
            else:
                self.amount -= self.bank.withdraw_transaction(cash)
        else:
            print("Ошибка. Окончание времени депозита не наступило.")


class CreditAccount(Account):
    def __init__(self, ident, bank: Bank, limit, credit_cash, terms: Terms, user: User):
        super().__init__(ident, bank, user, terms)
        self.limit = limit  # должен быть отрицательным

    # снятие
    def withdraw_comission(self):
        transaction = Transaction(amount=self.terms.commission, fromAcc=self, id="123")  # todo: add bank account
        self.amount -= self.bank.withdraw_transaction(transaction)

    # снятие средств со счета
    def withdraw(self, cash):
        transaction = Transaction(amount=cash, fromAcc=self, id="123")
        if self.amount - cash < self.limit:
            print("Ошибка. Превышен лимит")
            return
        elif self.amount - cash < 0:
            self.amount -= cash
            self.withdraw_comission()
        self.bank.withdraw_transaction(transaction)

