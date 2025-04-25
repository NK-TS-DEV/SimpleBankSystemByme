from datetime import datetime


class Transaction:
    transaction_id: int
    amount: float
    transaction_type: str
    time_stamp: datetime
    currency: str

    def __init__(self, transaction_id: int, amount: float, transaction_type: str, time_stamp: datetime,currency)-> None:
        self.transaction_id = transaction_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.time_stamp = time_stamp
        self.currency = currency

    def get_transaction_id(self) -> int:
        return self.transaction_id

    def get_transaction_type(self) -> str:
        return f'{self.transaction_type}'

    def get_transaction_detail(self)-> str:
        return f'Amount: {self.amount} Currency {self.currency}, Transaction type: {self.transaction_type}, Time= {self.time_stamp}'

    def __repr__(self):
        return f"Transaction(ID={self.transaction_id}, Type={self.transaction_type}, Amount={self.amount}, Time={self.time_stamp})"

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "transaction_type": self.transaction_type,
            "currency": self.currency,
            "time_stamp": self.time_stamp.isoformat()
        }



    @staticmethod
    def from_dict(data):
        return Transaction(
            transaction_id=data["transaction_id"],
            amount=data["amount"],
            transaction_type=data["transaction_type"],
            currency=data["currency"],
            time_stamp=datetime.fromisoformat(data["time_stamp"])
        )