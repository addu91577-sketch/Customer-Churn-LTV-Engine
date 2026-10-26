"""
Customer Churn & LTV Engine - Database Ingestion Pipeline (Week 1: Days 1–2)
Connects to PostgreSQL (Data Warehouse) via SQLAlchemy to ingest sanitized Telco customer data.
Includes automatic fallback to SQLite for local lightweight testing.
Author: Adarsh Kumar Pandey
"""

import os
import argparse
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, Float, String, text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customers'

    customerID = Column(String(50), primary_key=True)
    gender = Column(String(20))
    SeniorCitizen = Column(Integer)
    Partner = Column(String(10))
    Dependents = Column(String(10))
    tenure = Column(Integer)
    PhoneService = Column(String(10))
    MultipleLines = Column(String(20))
    InternetService = Column(String(20))
    OnlineSecurity = Column(String(20))
    OnlineBackup = Column(String(20))
    DeviceProtection = Column(String(20))
    TechSupport = Column(String(20))
    StreamingTV = Column(String(20))
    StreamingMovies = Column(String(20))
    Contract = Column(String(20))
    PaperlessBilling = Column(String(10))
    PaymentMethod = Column(String(50))
    MonthlyCharges = Column(Float)
    TotalCharges = Column(Float)
    Churn = Column(String(10))


def ingest_data(db_url: str = None, csv_path: str = 'data/telco_customer_churn_clean.csv', use_sqlite: bool = False):
    if use_sqlite or db_url is None:
        db_url = "sqlite:///data/customer_churn_db.sqlite"

    print(f"Connecting to database via SQLAlchemy: {db_url}")
    engine = create_engine(db_url)

    print("Creating table schema if not present...")
    Base.metadata.create_all(engine)

    print(f"Reading sanitized customer dataset from {csv_path}...")
    df = pd.read_csv(csv_path)

    print(f"Ingesting {len(df)} records into 'customers' table...")
    df.to_sql('customers', con=engine, if_exists='replace', index=False)

    # Verification query
    with engine.connect() as conn:
        res = conn.execute(text("SELECT count(*) FROM customers"))
        count = res.scalar()
        print(f"[SUCCESS] Ingestion verified! Total records in database table 'customers': {count}")

    return count


def main():
    parser = argparse.ArgumentParser(description="Ingest Telco data into PostgreSQL / SQLite Data Warehouse")
    parser.add_argument('--db-url', default=None, help="Database connection URI (e.g. postgresql://user:pass@localhost:5432/customer_churn_db)")
    parser.add_argument('--csv', default='data/telco_customer_churn_clean.csv', help="Path to sanitized CSV")
    parser.add_argument('--sqlite', action='store_true', default=False, help="Use local SQLite database fallback")
    args = parser.parse_args()

    ingest_data(db_url=args.db_url, csv_path=args.csv, use_sqlite=args.sqlite)


if __name__ == '__main__':
    main()
