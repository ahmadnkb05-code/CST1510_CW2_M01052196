"""
models.py
Simple dataclasses + CRUD functions that call databasemanager.
"""

from dataclasses import dataclass
from typing import Dict, Any
from db_manager import DatabaseManager

db = DatabaseManager()


@dataclass
class User:
    username: str
    password_hash_hex: str
    role: str


@dataclass
class SecurityIncident:
    incident_id: str
    category: str
    severity: int
    status: str
    reported_at: str = None
    resolved_at: str = None
    resolution_time_mins: int = None


@dataclass
class ITTicket:
    ticket_id: str
    staff: str
    status: str
    created_at: str = None
    resolved_at: str = None
    resolution_time_mins: int = None


# --- Users ---
def insert_user(username: str, password_hash_hex: str, role: str):
    db.create_tables()
    db.execute(
        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?);",
        (username, password_hash_hex, role),
    )


# --- Cyber incidents CRUD ---
def create_cyber_incident(inc: SecurityIncident):
    db.create_tables()
    db.execute(
        """INSERT INTO cyber_incidents
           (incident_id, category, severity, status, reported_at, resolved_at, resolution_time_mins)
           VALUES (?, ?, ?, ?, ?, ?, ?);""",
        (inc.incident_id, inc.category, inc.severity, inc.status,
         inc.reported_at, inc.resolved_at, inc.resolution_time_mins)
    )


def read_cyber_incidents(limit=200):
    return db.query("SELECT * FROM cyber_incidents ORDER BY reported_at DESC LIMIT ?;", (limit,))


def update_cyber_incident(id_: int, updates: Dict[str, Any]):
    allowed = ["incident_id", "category", "severity", "status",
               "reported_at", "resolved_at", "resolution_time_mins"]
    keys = [k for k in updates.keys() if k in allowed]
    if not keys:
        return
    set_clause = ", ".join([f"{k} = ?" for k in keys])
    params = tuple(updates[k] for k in keys) + (id_,)
    db.execute(f"UPDATE cyber_incidents SET {set_clause} WHERE id = ?;", params)


def delete_cyber_incident(id_: int):
    db.execute("DELETE FROM cyber_incidents WHERE id = ?;", (id_,))


# --- IT tickets CRUD ---
def create_ticket(t: ITTicket):
    db.create_tables()
    db.execute(
        """INSERT INTO it_tickets
           (ticket_id, staff, status, created_at, resolved_at, resolution_time_mins)
           VALUES (?, ?, ?, ?, ?, ?);""",
        (t.ticket_id, t.staff, t.status, t.created_at, t.resolved_at, t.resolution_time_mins)
    )


def read_tickets(limit=200):
    return db.query("SELECT * FROM it_tickets ORDER BY created_at DESC LIMIT ?;", (limit,))


def update_ticket(id_: int, updates: Dict[str, Any]):
    allowed = ["ticket_id", "staff", "status", "created_at", "resolved_at", "resolution_time_mins"]
    keys = [k for k in updates.keys() if k in allowed]
    if not keys:
        return
    set_clause = ", ".join([f"{k} = ?" for k in keys])
    params = tuple(updates[k] for k in keys) + (id_,)
    db.execute(f"UPDATE it_tickets SET {set_clause} WHERE id = ?;", params)


def delete_ticket(id_: int):
    db.execute("DELETE FROM it_tickets WHERE id = ?;", (id_,))
