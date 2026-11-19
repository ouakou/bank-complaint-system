
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Account_test:
    def __init__(self, row):
        self.account_id = row["account_id"]
        self.customer_id = row["customer_id"]
        self.account_number = row["account_number"]
        self.account_type = row["account_type"]
        self.status = row["status"]
        self.current_balance = row["current_balance"]
        self.opened_date = row["opened_date"]


class Account(SQLModel, table=True):
    __tablename__ = "account"

    account_id: str = Field(primary_key=True)
    customer_id: str = Field(foreign_key="customer.customer_id")
    account_number: str
    account_type: str
    status: str
    current_balance: float
    opened_date: str

    