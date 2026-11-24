"""In-memory fakes for unit and API tests (Exercise 3.1.2). No database needed.

    store = FakeStore.sample()
    service = make_service(store, today=lambda: date(2026, 9, 1))

ComplaintService builds its own repositories from the session it is given, so
make_service creates it with FakeDB(store) and then swaps in fake_repositories(store).

FakeDB.transaction() copies the store first and puts the copy back if the block
raises, so the fakes roll back like the real database does.

The fakes mirror the real repositories (same methods and arguments) and return the
real SQLModel objects (Complaint, Customer, Account, ComplaintStatusHistory), built
in memory, so the service can use attribute access like complaint.status.
"""
import copy
from contextlib import contextmanager
from datetime import date

# Importing every model registers all tables, so SQLModel can build the objects.
from Models.account import Account
from Models.complaint import Complaint
from Models.complaint_status_history import ComplaintStatusHistory
from Models.customer import Customer
import Models.employee  # noqa: F401

from Service.complaint_services.services import ComplaintService, Repositories


class FakeStore:
    def __init__(self):
        self.customers, self.accounts, self.complaints = {}, {}, {}
        self.history, self.requests = [], []

    @classmethod
    def sample(cls):
        s = cls()
        s.customers["CUS001"] = Customer(customer_id="CUS001", first_name="Taylor", last_name="Wilson",
                                         email="taylor@example.com", phone_number="555-0100",
                                         segment="Premium")
        s.accounts["ACC001"] = Account(account_id="ACC001", customer_id="CUS001", account_number="1000001",
                                       account_type="Mortgage", status="ACTIVE", current_balance=0.0,
                                       opened_date="2020-01-01")
        for cid, status in [("CMP001", "OPEN"), ("CMP002", "IN_PROGRESS"), ("CMP003", "UNDER_REVIEW"),
                            ("CMP004", "CLOSED"), ("CMP005", "PENDING_APPROVAL")]:
            s.complaints[cid] = Complaint(complaint_id=cid, customer_id="CUS001", account_id=None,
                                          channel="Web", category="Fee Dispute", complaint_text="Sample",
                                          priority="Medium", status=status,
                                          received_at="2026-08-01 09:00:00", assigned_analyst_id=None)
            s.history.append(ComplaintStatusHistory(history_id=len(s.history) + 1, complaint_id=cid,
                                                    old_status=None, new_status=status,
                                                    changed_at="2026-08-01 09:00:00",
                                                    changed_by=None, comments="Complaint created"))
        return s


class FakeDB:
    def __init__(self, store):
        self.store = store

    @contextmanager
    def transaction(self):
        saved = copy.deepcopy(self.store.__dict__)
        try:
            yield None
        except Exception:
            self.store.__dict__.clear()
            self.store.__dict__.update(saved)
            raise


class FakeCustomers:
    def __init__(self, s): self.s = s
    def get_by_id(self, customer_id): return self.s.customers.get(customer_id)


class FakeAccounts:
    def __init__(self, s): self.s = s
    def get_for_customer(self, customer_id):
        return sorted((a for a in self.s.accounts.values() if a.customer_id == customer_id),
                      key=lambda a: a.account_id)


class FakeComplaints:
    def __init__(self, s): self.s = s

    def get_by_id(self, complaint_id):
        return self.s.complaints.get(complaint_id)

    def get_for_complaint(self, customer_id):
        return [c for c in self.s.complaints.values() if c.customer_id == customer_id]

    def next_id(self):
        highest = max((int(cid[3:]) for cid in self.s.complaints), default=0)
        return f"CMP{highest + 1:03d}"

    def create(self, complaint_id, customer_id, channel, category, complaint_text, priority, status,
               received_at, assigned_analyst_id=None, account_id=None):
        complaint = Complaint(complaint_id=complaint_id, customer_id=customer_id, account_id=account_id,
                              channel=channel, category=category, complaint_text=complaint_text,
                              priority=priority, status=status, received_at=received_at,
                              assigned_analyst_id=assigned_analyst_id)
        self.s.complaints[complaint_id] = complaint
        return complaint

    def update_status(self, complaint_id, status):
        complaint = self.s.complaints[complaint_id]
        complaint.status = status
        return complaint


class FakeHistory:
    def __init__(self, s): self.s = s

    def get_for_complaint(self, complaint_id):
        rows = [h for h in self.s.history if h.complaint_id == complaint_id]
        return sorted(rows, key=lambda h: (h.changed_at, h.history_id))

    def add(self, complaint_id, old_status, new_status, changed_at, changed_by_role, comments):
        history = ComplaintStatusHistory(history_id=len(self.s.history) + 1, complaint_id=complaint_id,
                                         old_status=old_status, new_status=new_status,
                                         changed_by=changed_by_role, changed_at=changed_at,
                                         comments=comments)
        self.s.history.append(history)
        return history


class FakeRequests:
    """Rows are (request_id, request_type, status, created_at) tuples, like the real query."""
    def __init__(self, s): self.s = s
    def get_for_complaint(self, complaint_id):
        return [(r["request_id"], r["request_type"], r["status"], r["created_at"])
                for r in self.s.requests if r["complaint_id"] == complaint_id]


def fake_repositories(store):
    return lambda _conn: Repositories(FakeCustomers(store), FakeAccounts(store), FakeComplaints(store),
                                      FakeHistory(store), FakeRequests(store))


def make_service(store, today=date.today):
    """A ComplaintService wired to the in-memory store."""
    service = ComplaintService(FakeDB(store), today=today)
    repos = fake_repositories(store)(service.session)
    service.customers = repos.customers
    service.accounts = repos.accounts
    service.complaints = repos.complaints
    service.history = repos.history
    service.requests = repos.requests
    return service
