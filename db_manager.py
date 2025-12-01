"""
db_manager.py
One small class to:
open a connection to SQLite (multi_domain.db)
can run queries safely
create the 3 tables we need (users, cyber_incidents, it_tickets)
"""

import sqlite3
from pathlib import Path
from typing import Optional, Tuple, List

# Database file path
DB_PATH = Path("multi_domain.db")


class DatabaseManager:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None

    def connect(self):
        """Connect to the SQLite database."""
        if not self.conn:
            self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self.conn.row_factory = sqlite3.Row  # rows behave like dicts

    def close(self):
        """Commit and close connection."""
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def execute(self, sql: str, params: Tuple = ()):
        """Run INSERT/UPDATE/DELETE queries."""
        self.connect()
        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        return cur

    def query(self, sql: str, params: Tuple = ()) -> List[sqlite3.Row]:
        """Run SELECT queries and return results."""
        self.connect()
        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()

    def create_tables(self):
        """Create the tables if they don’t already exist."""

        # Users table
        self.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        );
        """)

        # Cybersecurity incidents table
        self.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_id TEXT NOT NULL,
            category TEXT NOT NULL,
            severity INTEGER NOT NULL,
            status TEXT NOT NULL,
            reported_at TEXT,
            resolved_at TEXT,
            resolution_time_mins INTEGER
        );
        """)

        # IT tickets table
        self.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT NOT NULL,
            staff TEXT,
            status TEXT,
            created_at TEXT,
            resolved_at TEXT,
            resolution_time_mins INTEGER
        );
        """)