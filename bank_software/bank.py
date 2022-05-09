import uuid
import typing
import dataclasses

from singleton_decorator import singleton

from .errors import *
from .transaction import Transaction
from .user import User


@dataclasses.dataclass
class Bank:
    id: uuid.UUID

    users: typing.Dict[uuid.UUID, User]
    user_mapping: typing.Dict[int, uuid.UUID]

    transactions: typing.Dict[uuid.UUID, Transaction]

    def create_user(self, user: User) -> User:
        if hash(user) in self.user_mapping:
            raise UserAlreadyExists

        self.users[user.id] = user
        self.user_mapping[hash(user)] = user.id
        user.bank_id = self.id

        return user

    def update_user(self, user: User) -> User:
        if user.id not in self.users:
            raise UserNotFound

        self.users[user.id] = user

        return user

    def get_user(self, user: User) -> User:
        if hash(user) not in self.user_mapping:
            raise UserNotFound

        return self.users[self.user_mapping[hash(user)]]

    def add_transaction(self, transaction: Transaction):
        if transaction.id in self.transactions:
            raise TransactionAlreadyExists
        self.transactions[transaction.id] = transaction

    def withdraw_transaction(self, transaction: Transaction):
        if transaction.id not in self.transactions:
            raise TransactionAlreadyExists  # todo: change error
        self.transactions.pop(transaction.id)


@dataclasses.dataclass
@singleton
class BankManager:
    banks: typing.Dict[uuid.UUID, Bank] = {}

    def get_bank(self, id: uuid.UUID) -> Bank:
        if id not in self.banks:
            raise BankNotFound

        return self.banks[id]
