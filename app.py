import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
from pathlib import Path
from utils.villain import Villain
from utils.hero import Hero
from utils.analyst import Analyst
from utils.safety import SafetyEnforcer
from utils.config import Config

# --- Page Config ---
st.set_page_config(
    page_title="Ransomware Resilience Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Premium Aesthetics ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #1f2937;
        border: 1px solid #374151;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    div[data-testid="stMetric"] label {
        color: #9ca3af;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #60a5fa;
    }
    
    /* Buttons */
    .stButton button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    /* Attack Button */
    div[data-testid="stButton"] button:has(div:contains("Simulate Ransomware Attack")) {
        background-color: #ef4444;
        color: white;
        border: none;
    }
    div[data-testid="stButton"] button:has(div:contains("Simulate Ransomware Attack")):hover {
        background-color: #dc2626;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.5);
    }

    /* Restore Button */
    div[data-testid="stButton"] button:has(div:contains("Initiate Disaster Recovery")) {
        background-color: #10b981;
        color: white;
        border: none;
    }
    div[data-testid="stButton"] button:has(div:contains("Initiate Disaster Recovery")):hover {
        background-color: #059669;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.5);
    }
    
    /* Reset Button */
    div[data-testid="stButton"] button:has(div:contains("Reset Simulation Environment")) {
        background-color: #4b5563;
        color: white;
        border: none;
    }
    div[data-testid="stButton"] button:has(div:contains("Reset Simulation Environment")):hover {
        background-color: #374151;
    }
    
    /* Status Indicators */
    .status-healthy {
        color: #10b981;
        font-weight: bold;
        padding: 4px 8px;
        background: rgba(16, 185, 129, 0.1);
        border-radius: 4px;
    }
    .status-infected {
        color: #ef4444;
        font-weight: bold;
        padding: 4px 8px;
        background: rgba(239, 68, 68, 0.1);
        border-radius: 4px;
    }
    
    /* Ransom Note Style */
    .ransom-note {
        background-color: #7f1d1d;
        color: #fecaca;
        padding: 20px;
        border: 2px dashed #ef4444;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        margin-bottom: 20px;
    }
    
    /* File Viewer */
    .file-viewer {
        background-color: #111827;
        border: 1px solid #374151;
        padding: 10px;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
        color: #d1d5db;
        max-height: 200px;
        overflow-y: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Initialization ---
if 'initialized' not in st.session_state:
    Hero.generate_dummy_data()
    st.session_state['initialized'] = True

# --- Sidebar ---
with st.sidebar:
    st.title("🛡️ SecOps Control")
    st.markdown("---")
    st.markdown("""
    **System Status:**  
    Monitoring active directory:  
    `./production_data`
    """)
    
    st.info("""
    **ISO 27001 Context:**
    This dashboard demonstrates **Business Continuity** and **Resilience**.
    
    **RTO (Recovery Time Objective):**
    The targeted duration of time and a service level within which a business process must be restored after a disaster.
    """)
    
    st.markdown("---")
    st.subheader("⚙️ Admin Actions")
    if st.button("Reset Simulation Environment"):
        with st.spinner("Resetting environment..."):
            Hero.generate_dummy_data()
            time.sleep(0.5)
            st.toast("Environment Reset Successfully", icon="✅")
            time.sleep(1)
            st.rerun()

# --- Main Content ---
st.title("Ransomware Resilience & RTO Dashboard")
st.markdown("### Real-time Incident Response Drill")

# Metrics Row
col1, col2, col3 = st.columns(3)

# Calculate Metrics
logs = Analyst.get_logs()
last_rto_val, last_incident_id = Analyst.calculate_last_rto()
files = list(Config.PRODUCTION_DIR.glob("*"))
encrypted_files = [f for f in files if f.suffix == ".locked"]
ransom_note = Config.PRODUCTION_DIR / Config.RANSOM_NOTE_FILE
is_compromised = len(encrypted_files) > 0 or ransom_note.exists()

with col1:
    st.metric("System Health", "Compromised" if is_compromised else "Healthy", delta="-CRITICAL" if is_compromised else "Secure", delta_color="inverse")

with col2:
    rto_display = f"{last_rto_val:.2f}s" if last_rto_val else "N/A"
    st.metric("Last RTO (Recovery Time)", rto_display, help="Time taken to restore operations after the last attack.")

with col3:
    st.metric("Files Monitored", len(files))

st.markdown("---")

# Ransom Note Alert
if is_compromised and ransom_note.exists():
    with open(ransom_note, "r") as f:
        note_content = f.read()
    st.markdown(f'<div class="ransom-note">⚠️ SECURITY ALERT: RANSOM NOTE DETECTED ⚠️<br><br>{note_content}</div>', unsafe_allow_html=True)

# Control Center
c1, c2 = st.columns(2)

with c1:
    st.subheader("🔴 Red Team (Attack)")
    if st.button("Simulate Ransomware Attack", use_container_width=True, disabled=is_compromised):
        progress_bar = st.progress(0, text="Initializing Attack Vector...")
        
        def update_progress(p):
            progress_bar.progress(p, text=f"Encrypting Filesystem... {int(p*100)}%")
            
        count, incident_id = Villain.infect_system(progress_callback=update_progress)
        progress_bar.progress(1.0, text="Encryption Complete.")
        time.sleep(0.5)
        st.toast(f"ATTACK SUCCESSFUL: {count} files encrypted.", icon="💀")
        st.rerun()

with c2:
    st.subheader("🟢 Blue Team (Defense)")
    if st.button("Initiate Disaster Recovery", use_container_width=True, disabled=not is_compromised):
        progress_bar = st.progress(0, text="Initializing Recovery Protocols...")
        
        def update_progress(p):
            progress_bar.progress(p, text=f"Restoring from Immutable Backup... {int(p*100)}%")
            
        count = Hero.restore_operations(progress_callback=update_progress)
        progress_bar.progress(1.0, text="Recovery Complete.")
        time.sleep(0.5)
        st.toast(f"RECOVERY COMPLETE: {count} files restored.", icon="🛡️")
        st.balloons()
        time.sleep(1)
        st.rerun()

# RTO Trends Chart
st.markdown("### 📈 RTO Performance Trends")
rto_history = Analyst.get_rto_history()
if rto_history:
    df_rto = pd.DataFrame(rto_history)
    fig = px.line(df_rto, x="date", y="rto_seconds", markers=True, title="Recovery Time Objective (RTO) Over Time")
    fig.update_layout(
        xaxis_title="Drill Date",
        yaxis_title="RTO (Seconds)",
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No RTO data available yet. Run a drill to generate metrics.")

# File System View & Forensics
st.markdown("### 📂 Live File System Forensics")

# Create a layout for file list and file preview
f_col1, f_col2 = st.columns([3, 2])

with f_col1:
    file_data = []
    for f in files:
        status = "🔒 Encrypted" if f.suffix == ".locked" else "✅ Healthy"
        if f.name == Config.RANSOM_NOTE_FILE:
            status = "⚠️ Ransom Note"
            
        file_data.append({
            "File Name": f.name,
            "Status": status,
            "Size": f"{f.stat().st_size} B",
            "path": str(f) # Hidden column for selection logic
        })

    if file_data:
        df = pd.DataFrame(file_data)
        
        # Custom styling for the dataframe
        def color_status(val):
            if 'Encrypted' in val:
                return 'color: #ef4444; font-weight: bold'
            elif 'Ransom Note' in val:
                return 'color: #f59e0b; font-weight: bold'
            else:
                return 'color: #10b981; font-weight: bold'

        st.dataframe(
            df.style.map(color_status, subset=['Status']),
            use_container_width=True,
            hide_index=True,
            column_config={"path": None} # Hide path
        )
    else:
        st.warning("No files found in production directory.")

with f_col2:
    st.markdown("**🔍 File Content Inspector**")
    selected_file = st.selectbox("Select a file to inspect:", [f["File Name"] for f in file_data] if file_data else [])
    
    if selected_file:
        file_path = Config.PRODUCTION_DIR / selected_file
        if file_path.exists():
            try:
                # Read first 500 bytes
                with open(file_path, "rb") as f:
                    content_bytes = f.read(500)
                    
                try:
                    content_str = content_bytes.decode('utf-8')
                except UnicodeDecodeError:
                    content_str = str(content_bytes) # Show raw bytes representation if binary/encrypted
                
                st.markdown(f"**Preview: `{selected_file}`**")
                st.markdown(f'<div class="file-viewer">{content_str}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Could not read file: {e}")

# Drill History Log
with st.expander("View Detailed Drill Logs"):
    if logs:
        # Reverse logs to show newest first
        log_df = pd.DataFrame(logs).iloc[::-1]
        st.dataframe(log_df, use_container_width=True, hide_index=True)
    else:
        st.info("No drills recorded yet.")
