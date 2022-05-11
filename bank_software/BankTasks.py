from .Time import Time
import sys
from .Account import Account
from .Account import CreditAccount
from .Account import DebtAccount
from .Account import DepositAccount


class BankTasks:
    
    def __init__(self):
        self.debtamount = DebtAccount().amount
        self.depositamount = DepositAccount().amount
        self.creditamount = CreditAccount().amount
        
        
    def onDebtDayEnd(self):
        debtamount_time = Time().now()
        
        if (Time().now() >= DebtAccount().starttime) :
            Account.amount += self.debtamount
            self.debtamount == 0
        else:
            self.debtamount += Account().calcDebtDailyPercent()
            
        return self.debtamount


    def onCreditDayEnd(self):
        creditamount_time = Time().now()
         
        if CreditAccount().amount == 0 :
            self.creditamount = 0
            sys.exit('Кредит выплачен')
        else:
            if Account.amount <= 0 :
                self.debtamount = DebtAccount().amount
                sys.exit('Недостаточно средств для списания')
            else:
                self.creditamount -= Account().calcCreditDailyPercent()
                Account().amount -= Account().calcCreditDailyPercent()
        
        return self.creditamount
            
                    
    def onDepositDayEnd(self):
        return self.depositamount
    
    
            
         
    def onDebtMonthEnd(self):
        debtamount_time = Time().now()
        
        if (Time().now() >= DebtAccount().starttime) :
            Account.amount += self.debtamount
            self.debtamount == 0
        else:
            self.debtamount += Account().calcDebtDailyPercent()
            
        return self.debtamount


    def onCreditMonthEnd(self):
        creditamount_time = Time().now()
         
        if CreditAccount().amount == 0 :
            self.creditamount = 0
            sys.exit('Кредит выплачен')
        else:
            if Account.amount <= 0 :
                self.debtamount = DebtAccount().amount
                sys.exit('Недостаточно средств для списания')
            else:
                self.creditamount -= Account().calcCreditMonthlyPercent()
                Account().amount -= Account().calcCreditMonthlyPercent()
        
        return self.creditamount
            
                    
    def onDepositMonthEnd(self):
        return self.depositamount
    
