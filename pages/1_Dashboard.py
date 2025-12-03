"""
Week 8-9: Dashboard with Database Integration
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.data.db import get_all_incidents, get_all_datasets, get_all_tickets

# Only set page config if running standalone
if "logged_in" not in st.session_state:
    st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
    st.warning("Please login first")
    st.stop()

# Check authentication
if not st.session_state.get("logged_in", False):
    st.warning("Please login first")
    st.stop()

# Header
st.title("📊 Intelligence Dashboard")
st.markdown(f"**User:** {st.session_state.username}")

# Navigation
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    if st.button("🏠 Home"):
        st.session_state.page = "home"
        st.rerun()
with col2:
    if st.button("🤖 AI Assistant"):
        st.session_state.page = "chatgpt"
        st.rerun()

st.divider()

# Tabs for different data views
tab1, tab2, tab3 = st.tabs(["🔴 Cyber Incidents", "📁 Datasets", "🎫 IT Tickets"])

# CYBER INCIDENTS TAB
with tab1:
    st.subheader("Cyber Security Incidents")
    
    incidents = get_all_incidents()
    if incidents:
        # Convert to DataFrame properly
        df = pd.DataFrame([dict(row) for row in incidents])
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Incidents", len(df))
        with col2:
            high_count = len(df[df['severity'].astype(str).str.lower() == 'high']) if 'severity' in df.columns else 0
            st.metric("High Severity", high_count)
        with col3:
            resolved_count = len(df[df['status'].astype(str).str.lower() == 'resolved']) if 'status' in df.columns else 0
            st.metric("Resolved", resolved_count)
        
        st.divider()
        
        # Data table - show all columns
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Charts
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("By Severity")
            if 'severity' in df.columns:
                severity_counts = df['severity'].value_counts()
                st.bar_chart(severity_counts)
        
        with col2:
            st.subheader("By Status")
            if 'status' in df.columns:
                status_counts = df['status'].value_counts()
                st.bar_chart(status_counts)
    else:
        st.info("No incidents found in database")

# DATASETS TAB
with tab2:
    st.subheader("Dataset Metadata")
    
    datasets = get_all_datasets()
    if datasets:
        df = pd.DataFrame([dict(row) for row in datasets])
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Datasets", len(df))
        with col2:
            if 'rows' in df.columns:
                total_rows = df['rows'].sum()
                st.metric("Total Rows", f"{int(total_rows):,}")
            else:
                st.metric("Total Rows", "N/A")
        with col3:
            if 'columns' in df.columns:
                total_cols = df['columns'].sum()
                st.metric("Total Columns", int(total_cols))
            else:
                st.metric("Total Columns", "N/A")
        
        st.divider()
        
        # Data table
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Chart
        st.subheader("Dataset Rows")
        if 'rows' in df.columns and 'name' in df.columns:
            chart_data = df.set_index('name')['rows']
            st.bar_chart(chart_data)
        else:
            st.info("Row data not available")
    else:
        st.info("No datasets found in database")

# IT TICKETS TAB
with tab3:
    st.subheader("IT Support Tickets")
    
    tickets = get_all_tickets()
    if tickets:
        df = pd.DataFrame([dict(row) for row in tickets])
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tickets", len(df))
        with col2:
            if 'priority' in df.columns:
                high_count = len(df[df['priority'].astype(str).str.lower() == 'high'])
                st.metric("High Priority", high_count)
            else:
                st.metric("High Priority", "N/A")
        with col3:
            if 'status' in df.columns:
                resolved_count = len(df[df['status'].astype(str).str.lower() == 'resolved'])
                st.metric("Resolved", resolved_count)
            else:
                st.metric("Resolved", "N/A")
        
        st.divider()
        
        # Data table
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Charts
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("By Priority")
            if 'priority' in df.columns:
                priority_counts = df['priority'].value_counts()
                st.bar_chart(priority_counts)
        
        with col2:
            st.subheader("By Status")
            if 'status' in df.columns:
                status_counts = df['status'].value_counts()
                st.bar_chart(status_counts)
    else:
        st.info("No tickets found in database")
