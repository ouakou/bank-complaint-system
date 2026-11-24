import sqlite3
from sqlmodel import create_engine, Session
path = "/Users/ouafikouera/Documents/:Volumes:DBeaver Community:Volumes:DBeaver Community:DBeaver.app"
engine = create_engine(f"sqlite:///{path}")

def import_data_sqlite():
    with sqlite3.connect(path) as cn:
        cn.row_factory = sqlite3.Row
        complaint_rows = cn.execute("SELECT * FROM complaint").fetchall()
        account_rows = cn.execute("SELECT * FROM account").fetchall()
        customer_rows = cn.execute("SELECT * FROM customer").fetchall()
    return complaint_rows, account_rows, customer_rows



def get_session():
    with Session(engine) as session:
        yield session