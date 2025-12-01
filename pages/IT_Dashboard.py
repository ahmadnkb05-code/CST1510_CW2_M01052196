import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime
from models import read_tickets, create_ticket, update_ticket, delete_ticket, ITTicket

st.set_page_config(page_title="IT Dashboard")
st.title("IT Tickets Dashboard")

if "user" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

rows = read_tickets(limit=500)
df = pd.DataFrame([dict(r) for r in rows]) if rows else pd.DataFrame([])

st.write("Logged in as:", st.session_state["user"]["username"])
st.write("Total tickets:", len(df))

if not df.empty:
    status_counts = df["status"].value_counts().reset_index()
    status_counts.columns = ["status", "count"]
    st.plotly_chart(px.pie(status_counts, names="status", values="count", title="Tickets by Status"),
                    use_container_width=True)

    rt = df.dropna(subset=["resolution_time_mins"])
    if not rt.empty:
        avg = rt.groupby("staff")["resolution_time_mins"].mean().reset_index()
        st.plotly_chart(px.bar(avg, x="staff", y="resolution_time_mins",
                               title="Avg Resolution Time by Staff (mins)"),
                        use_container_width=True)

st.markdown("---")
st.subheader("Create ticket")
with st.form("create_ticket"):
    tid = st.text_input("Ticket ID", value=f"TKT{int(datetime.utcnow().timestamp())%10000}")
    staff = st.text_input("Staff", value="unassigned")
    status = st.selectbox("Status", ["Open", "In Progress", "Waiting for User", "Resolved", "Closed"])
    go = st.form_submit_button("Create")
    if go:
        create_ticket(ITTicket(tid, staff, status, created_at=datetime.utcnow().isoformat()))
        st.success("Ticket created. Refresh to see it.")

st.markdown("---")
st.subheader("Update / Delete")
with st.form("upd_del"):
    id_s = st.text_input("Row id (from DB)")
    action = st.selectbox("Action", ["Update", "Delete"])
    if action == "Update":
        field = st.selectbox("Field", ["ticket_id", "staff", "status", "resolved_at", "resolution_time_mins"])
        value = st.text_input("New value")
    go2 = st.form_submit_button("Apply")
    if go2:
        try:
            rid = int(id_s)
            if action == "Delete":
                delete_ticket(rid)
                st.success("Deleted (if existed).")
            else:
                v = int(value) if field == "resolution_time_mins" and value else value or None
                update_ticket(rid, {field: v})
                st.success("Updated (if existed).")
        except Exception as e:
            st.error(f"Error: {e}")
