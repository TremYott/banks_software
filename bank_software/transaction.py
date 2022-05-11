import dataclasses
import uuid

from . import Account


@dataclasses.dataclass
class Transaction:
    id: uuid.UUID

    amount: float

    fromAcc: Account
    toAcc: Account
