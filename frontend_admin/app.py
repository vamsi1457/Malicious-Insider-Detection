import streamlit as st
import pandas as pd
import sqlite3
import os
import time
from auth import check_password

# Page settings
st.set_page_config(page_title="MIDS Dashboard", page_icon="🛡️", layout="wide")

# Login successful ayithe ne ee lopaliki velthundi
if check_password():
    st.title("🛡️ Secure MIDS Admin Dashboard")
    st.markdown("Real-time Insider Threat Monitoring System")
    st.markdown("---")

    # 1. Database tho connect avvadam (Direct connection, no CSV!)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "..", "backend_api", "database", "insider_threats.db")
    
    try:
        conn = sqlite3.connect(db_path)
        # Database nunchi latest 100 logs thechukuntunnam
        query = "SELECT * FROM system_logs ORDER BY timestamp DESC LIMIT 100"
        df = pd.read_sql(query, conn)
        conn.close()

        if not df.empty:
            # Metrics calculations
            total_logs = len(df)
            threats_df = df[df['is_threat'] == 1]
            total_threats = len(threats_df)
            
            # --- TOP METRICS ROW ---
            col1, col2, col3 = st.columns(3)
            col1.metric("Live Logs Analysed", total_logs)
            col2.metric("Safe Activities", total_logs - total_threats)
            col3.metric("🚨 Threats Detected", total_threats, delta_color="inverse")
            
            st.markdown("---")
            
            # --- THREAT ALERTS SECTION ---
            st.subheader("🚨 Active Threats")
            if total_threats > 0:
                for index, row in threats_df.iterrows():
                    st.error(f"**THREAT:** User `{row['user_id']}` performed `{row['action']}` at `{row['timestamp']}`. (Type: {row['threat_type']})")
            else:
                st.success("No active threats. Network is secure.")
                
            st.markdown("---")
            
            # --- LIVE DATA TABLE ---
            st.subheader("Live Network Traffic")
            display_df = df[['timestamp', 'user_id', 'ip_address', 'action', 'is_threat', 'threat_type']].copy()
            display_df['Status'] = display_df['is_threat'].apply(lambda x: '🔴 THREAT' if x == 1 else '🟢 NORMAL')
            
            # Show table without the raw boolean column
            st.dataframe(display_df.drop(columns=['is_threat']), use_container_width=True)
            
            # Live feel kosam prathi 3 seconds ki refresh avthundi
            time.sleep(3)
            st.rerun()

        else:
            st.info("Waiting for data... Start your data simulator!")

    except Exception as e:
        st.error(f"Cannot connect to database. Make sure API and DB are running. Error: {e}")