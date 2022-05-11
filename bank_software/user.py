import uuid
import typing
import dataclasses

from .bank import Bank, BankManager


@dataclasses.dataclass
class User:
    id: uuid.UUID

    name: str
    surname: str

    address: typing.Optional[str]
    passport: typing.Optional[str]

    bank_id: uuid.UUID

    def __hash__(self) -> int:
        return hash((self.name, self.surname))

    def is_suspicious(self) -> bool:
        return self.address is None or self.passport is None

    def get_bank(self) -> Bank:
        return BankManager().get_bank(self.bank_id)

    @staticmethod
    def create(**kwargs) -> "User":
        return User(
            uuid.uuid4(),
            kwargs["bank_id"],
            kwargs["user_name"],
            kwargs["user_surname"],
            kwargs.get("address", None),
            kwargs.get("passport", None),
        )
