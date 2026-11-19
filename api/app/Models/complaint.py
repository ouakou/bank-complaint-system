# complaint model class
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Complaint_test:
    def __init__(self, row):
        self.complaint_id = row["complaint_id"]
        self.customer_id = row["customer_id"]
        self.account_id = row["account_id"]
        self.category = row["category"]
        self.status = row["status"]
        self.received_at = row["received_at"]
        self.priority = row["priority"]


class Complaint(SQLModel, table=True):
    __tablename__ = "complaint"

    complaint_id: str = Field(primary_key=True)
    customer_id: str = Field(foreign_key="customer.customer_id")
    account_id: Optional[str] = Field(default=None, foreign_key="account.account_id")
    channel: str
    category: str
    complaint_text: str
    priority: Optional[str] = None
    status: str
    received_at: str
    assigned_analyst_id: Optional[str] = Field(default=None, foreign_key="employee.employee_id")

