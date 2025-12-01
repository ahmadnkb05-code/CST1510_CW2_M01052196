"""
load_sample_data.py
Adds a few simple rows so your dashboards have something to show.
"""

from datetime import datetime, timedelta
from models import SecurityIncident, ITTicket, create_cyber_incident, create_ticket
from db_manager import DatabaseManager


def create_samples():
    db = DatabaseManager()
    db.create_tables()
    now = datetime.utcnow()

    # Cyber incidents (tiny, readable)
    cyber = [
        SecurityIncident("INC001", "Phishing", 4, "Open",
                         reported_at=(now - timedelta(days=2)).isoformat()),
        SecurityIncident("INC002", "Malware", 5, "Resolved",
                         reported_at=(now - timedelta(days=10)).isoformat(),
                         resolved_at=(now - timedelta(days=9)).isoformat(),
                         resolution_time_mins=24*60),
        SecurityIncident("INC003", "Credential Theft", 3, "Investigating",
                         reported_at=(now - timedelta(days=1)).isoformat()),
    ]
    for c in cyber:
        create_cyber_incident(c)

    # IT tickets
    tickets = [
        ITTicket("TKT001", "Alice", "Resolved",
                 created_at=(now - timedelta(days=6)).isoformat(),
                 resolved_at=(now - timedelta(days=5)).isoformat(),
                 resolution_time_mins=24*60),
        ITTicket("TKT002", "Bob", "Waiting for User",
                 created_at=(now - timedelta(days=3)).isoformat()),
        ITTicket("TKT003", "Charlie", "In Progress",
                 created_at=(now - timedelta(days=1)).isoformat()),
    ]
    for t in tickets:
        create_ticket(t)

    print("✔ Sample data added.")


if __name__ == "__main__":
    create_samples()
