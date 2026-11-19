from sqlmodel import SQLModel, Field, Relationship
from typing import List

class Employee(SQLModel, table=True):
    __tablename__ = "employee"

    employee_id: str = Field(primary_key=True)
    first_name: str
    last_name: str
    email: str
    role: str
