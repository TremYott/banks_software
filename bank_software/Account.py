class Account:
    def __init__(self, ident, class_User, class_Terms):
        self.id=ident
        self.user=class_User
        self.amount=0
        self.percents_storage=[]
        self.percents=class_Terms.percents
        self.comission=class_Terms.comission
        self.restrictions=class_Terms.restrictions #этого не было на схеме
        self.sus_status=False

    def check_sus_status(self):
        if self.user.address & self.user.passport:
            self.sus_status=True

    def topUp(self, cash, class_Bank):
        self.amount+=class_Bank.Transaction_topUp(cash)
        # self.amount+=cash

        
    def withdraw(self, cash, class_Bank):
        if self.sus_status or cash<self.restrictions:
            if class_Bank.Transaction_withdraw(cash)>self.amount:
                print("Ошибка. Недостаточно средств")
            else:
                self.amount-=class_Bank.Transaction_withdraw(cash) 
        else:
            print("Ошибка. Заполните свои паспортные данные и/или адрес")


    def calcDailyPercent(self, class_BankTasks):
        self.percents_storage.append(class_BankTasks.onDayEnd*self.percents/100)

    def calcMonthlyPercent(self):
        self.amount+=sum(self.percents_storage)
        self.percents_storage=[]

class DebtAccount(Account):
    pass

class DepositAccount(Account):
    def __init__(self, ident, amount, duration):
        self.id=ident
        self.amount=amount
        self.duration=duration
        self.open_time=Time.now()
        self.percents_storage=[]
        self.restrictions=class_Terms.restrictions #этого не было на схеме
        self.sus_status=False
        if amount<=50000:
            self.percents=3
        elif amount<=100000:
            self.percents=3.5
        else:
            self.percents=4

    def withdraw(self, cash, class_Bank):
        if Time.now()-self.duration>=open_time:
            if class_Bank.Transaction_withdraw(cash)>self.amount:
                print("Ошибка. Недостаточно средств.")
            else:
                self.amount-=class_Bank.Transaction_withdraw(cash)
        else:
            print("Ошибка. Окончание времени депозита не наступило.")

class CreditAccount(Account):
    def __init__(self, ident, limit, credit_cash, class_Terms):
        self.id=ident
        self.amount=0
        self.restrictions=class_Terms.restrictions #этого не было на схеме
        self.sus_status=False
        self.limit=limit #должен быть отрицательным
        self.comission=class_Terms.comission
        self.status=False

    def withdraw_comission(self):
        if self.status:
            amount-=class_Bank.Transaction_withdraw(self.comission)
    
    def withdraw(self, cash, class_Bank):
        if amount-class_Bank.Transaction_withdraw(cash)<limit:
            print("Ошибка. Превышен лимит")
        elif amount-class_Bank.Transaction_withdraw(cash)<0:
            amount-=class_Bank.Transaction_withdraw(cash)
            self.status=True
