import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime
from models import (
    read_cyber_incidents, create_cyber_incident,
    update_cyber_incident, delete_cyber_incident, SecurityIncident
)

st.set_page_config(page_title="Cyber Dashboard")
st.title("Cybersecurity Dashboard")

if "user" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

rows = read_cyber_incidents(limit=500)
df = pd.DataFrame([dict(r) for r in rows]) if rows else pd.DataFrame([])

st.write("Logged in as:", st.session_state["user"]["username"])
st.write("Total incidents:", len(df))

if not df.empty:
    by_cat = df["category"].value_counts().reset_index()
    by_cat.columns = ["category", "count"]
    st.plotly_chart(px.bar(by_cat, x="category", y="count", title="Incidents by Category"), use_container_width=True)

    st.plotly_chart(px.histogram(df, x="severity", nbins=5, title="Severity distribution"), use_container_width=True)

    rt = df.dropna(subset=["resolution_time_mins"])
    if not rt.empty:
        avg = rt.groupby("category")["resolution_time_mins"].mean().reset_index()
        st.plotly_chart(px.bar(avg, x="category", y="resolution_time_mins",
                               title="Avg Resolution Time (mins) by Category"), use_container_width=True)

st.markdown("---")
st.subheader("Create new incident")
with st.form("create_incident"):
    iid = st.text_input("Incident ID", value=f"INC{int(datetime.utcnow().timestamp())%10000}")
    cat = st.text_input("Category", value="Phishing")
    sev = st.number_input("Severity (1-5)", 1, 5, 3)
    status = st.selectbox("Status", ["Open", "Investigating", "Resolved", "Closed"])
    submit = st.form_submit_button("Create")
    if submit:
        create_cyber_incident(
            SecurityIncident(iid, cat, int(sev), status, reported_at=datetime.utcnow().isoformat())
        )
        st.success("Incident created. Refresh page to see it.")

st.markdown("---")
st.subheader("Update / Delete")
with st.form("upd_del"):
    id_s = st.text_input("Row id (from DB)")
    action = st.selectbox("Action", ["Update", "Delete"])
    if action == "Update":
        field = st.selectbox("Field", ["category", "severity", "status", "resolved_at", "resolution_time_mins"])
        value = st.text_input("New value")
    go = st.form_submit_button("Apply")
    if go:
        try:
            rid = int(id_s)
            if action == "Delete":
                delete_cyber_incident(rid)
                st.success("Deleted (if existed).")
            else:
                v = int(value) if field in ["severity", "resolution_time_mins"] and value else value or None
                update_cyber_incident(rid, {field: v})
                st.success("Updated (if existed).")
        except Exception as e:
            st.error(f"Error: {e}")
