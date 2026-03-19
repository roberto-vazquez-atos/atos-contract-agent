"""DuckDB persistence layer for contract data."""
import duckdb
import os
import json
import uuid
from datetime import datetime


DB_PATH = os.getenv("DB_PATH", "data/contracts.duckdb")


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    encryption_key = os.getenv("DB_ENCRYPTION_KEY", "")
    config = {"encryption_key": encryption_key} if encryption_key else {}
    try:
        return duckdb.connect(DB_PATH, config=config)
    except Exception:
        # Encryption not supported by this DuckDB build — fall back to unencrypted
        return duckdb.connect(DB_PATH)


def initialize_schema():
    con = get_connection()
    con.execute("""
        CREATE TABLE IF NOT EXISTS raw_contracts (
            id VARCHAR PRIMARY KEY,
            filename VARCHAR,
            contract_type VARCHAR,
            raw_text TEXT,
            analyzed_at TIMESTAMP,
            file_size_bytes INTEGER,
            source_url VARCHAR,
            status VARCHAR DEFAULT 'Under Review'
        )
    """)
    # Migrate existing tables that predate source_url and status columns
    con.execute("ALTER TABLE raw_contracts ADD COLUMN IF NOT EXISTS source_url VARCHAR")
    con.execute("ALTER TABLE raw_contracts ADD COLUMN IF NOT EXISTS status VARCHAR DEFAULT 'Under Review'")
    con.execute("""
        CREATE TABLE IF NOT EXISTS raw_analyses (
            id VARCHAR PRIMARY KEY,
            contract_id VARCHAR,
            party_a VARCHAR,
            party_b VARCHAR,
            effective_date VARCHAR,
            expiration_date VARCHAR,
            governing_law VARCHAR,
            contract_value VARCHAR,
            risk_score INTEGER,
            risk_flags JSON,
            missing_clauses JSON,
            key_obligations JSON,
            summary TEXT,
            analyzed_at TIMESTAMP
        )
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS raw_clauses (
            id VARCHAR PRIMARY KEY,
            contract_id VARCHAR,
            clause_type VARCHAR,
            clause_text TEXT,
            present BOOLEAN,
            risk_level VARCHAR
        )
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS raw_audit_log (
            id VARCHAR PRIMARY KEY,
            action VARCHAR,
            filename VARCHAR,
            contract_type VARCHAR,
            performed_at TIMESTAMP,
            details TEXT
        )
    """)
    con.close()


def save_contract(contract_id: str, filename: str, contract_type: str,
                  raw_text: str, file_size: int, source_url: str = None, status: str = "Under Review"):
    con = get_connection()
    con.execute("""
        INSERT OR REPLACE INTO raw_contracts
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, [contract_id, filename, contract_type, raw_text,
          datetime.utcnow(), file_size, source_url, status])
    con.close()


def save_analysis(contract_id: str, analysis: dict):
    con = get_connection()
    con.execute("""
        INSERT OR REPLACE INTO raw_analyses
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        str(uuid.uuid4()),
        contract_id,
        analysis.get("party_a", ""),
        analysis.get("party_b", ""),
        analysis.get("effective_date", ""),
        analysis.get("expiration_date", ""),
        analysis.get("governing_law", ""),
        analysis.get("contract_value", ""),
        analysis.get("risk_score", 0),
        json.dumps(analysis.get("risk_flags", [])),
        json.dumps(analysis.get("missing_clauses", [])),
        json.dumps(analysis.get("key_obligations", [])),
        analysis.get("summary", ""),
        datetime.utcnow(),
    ])
    for clause in analysis.get("clauses", []):
        con.execute("""
            INSERT OR REPLACE INTO raw_clauses VALUES (?, ?, ?, ?, ?, ?)
        """, [
            str(uuid.uuid4()),
            contract_id,
            clause.get("type", ""),
            clause.get("text", ""),
            clause.get("present", False),
            clause.get("risk_level", "low"),
        ])
    con.close()


def log_audit_event(action: str, filename: str, contract_type: str, details: str = ""):
    """Record an audit trail entry for every analysis or comparison."""
    con = get_connection()
    con.execute("""
        INSERT INTO raw_audit_log VALUES (?, ?, ?, ?, ?, ?)
    """, [str(uuid.uuid4()), action, filename, contract_type, datetime.utcnow(), details])
    con.close()


def query(sql: str) -> "pd.DataFrame":
    import pandas as pd
    con = get_connection()
    result = con.execute(sql).df()
    con.close()
    return result


def contract_exists(contract_id: str) -> bool:
    con = get_connection()
    result = con.execute(
        "SELECT COUNT(*) FROM raw_contracts WHERE id = ?", [contract_id]
    ).fetchone()[0]
    con.close()
    return result > 0
