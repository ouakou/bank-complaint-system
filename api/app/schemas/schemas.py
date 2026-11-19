"""Request and response models (Exercise 3.2.2). Field names, enums and patterns
follow openapi v2.2.0. Response models list ONLY contract fields, so nothing extra
(email, risk_category, balances) can leak even if a repository returns it."""

from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from domain.models import Categrory as Category, Channel, ComplaintStatus, Priority

CUSTOMER_ID = r"^C[0-9]{4}$"
ACCOUNT_ID = r"^A[0-9]{5}$"
COMPLAINT_ID = r"^CP[0-9]{5}$"
EVIDENCE_REF = (r"^(CP[0-9]{5}|C[0-9]{4}|A[0-9]{5}|(KB-[0-9]{3}|BUL-[0-9]{4}-[0-9]{2})#c[0-9]{3}"
                r"|NOTE-[0-9]{6}|APR-[0-9]{6})$")


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")   # unknown fields -> 422 VALIDATION_ERROR


class Customer(Strict):
    customer_id: str
    first_name: str
    last_name: str
    segment: str


class StatusUpdateRequest(Strict):
    target_status: ComplaintStatus
    reason: str = Field(min_length=5, max_length=500)


class AccountSummary(Strict):
    account_id: str
    account_type: str
    status: str
    opened_date: str


class AccountList(Strict):
    customer_id: str
    accounts: List[AccountSummary]


class StatusHistoryRow(Strict):
    history_id: int
    old_status: Optional[str] = None
    new_status: str
    changed_by: Optional[str] = None
    changed_at: str
    comments: Optional[str] = None


class ServiceRequest(Strict):
    request_id: str
    request_type: str
    status: str
    created_at: str


class Complaint(Strict):
    complaint_id: str
    customer_id: str
    account_id: Optional[str] = None
    channel: str
    category: str
    complaint_text: str
    priority: Optional[str] = None
    status: str
    received_at: str
    assigned_analyst_id: Optional[str] = None
    status_history: List[StatusHistoryRow] = []
    service_requests: List[ServiceRequest] = []


class StatusUpdateResult(Strict):
    complaint_id: str
    old_status: str
    new_status: str
    audit_event_id: str


class Resolution(Strict):
    outcome: str = Field(min_length=3, max_length=100)
    compensation_cad: Decimal = Field(default=Decimal("0.00"), ge=0, decimal_places=2)
    notes: str = Field(min_length=5, max_length=500)


class CloseComplaintRequest(Strict):
    resolution: Resolution
    approval_ref: Optional[str] = Field(default=None, pattern=r"^APR-[0-9]{6}$")


class CloseComplaintResult(Strict):
    complaint_id: str
    old_status: str
    new_status: str
    audit_event_id: str
