from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class ComplaintStatusHistory(SQLModel, table=True):
    __tablename__ = "complaint_status_history"

    history_id: int = Field(default=None, primary_key=True)
    complaint_id: str = Field(foreign_key="complaint.complaint_id")
    old_status: str
    new_status: str
    changed_by: str = Field(foreign_key="employee.employee_id")
    changed_at: str
    comments: str

