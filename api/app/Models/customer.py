from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class Customer(SQLModel, table=True):
    __tablename__ = "customer"

    customer_id: str = Field(primary_key=True)
    first_name: str
    last_name: str
    email: str
    phone_number: str
    segment: str
    date_created: Optional[str] = None

  