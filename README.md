# 🛡️ Ransomware Resilience & RTO Dashboard

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![Security](https://img.shields.io/badge/Security-ISO%2027001-green)
![License](https://img.shields.io/badge/License-MIT-grey)

## 📋 Executive Summary

This project is a **Cyber Range Simulation** designed to demonstrate **Operational Resilience** and **Business Continuity** principles aligned with **ISO 27001** and the **Australian Essential Eight**.

It simulates a live ransomware attack on a sandboxed file system and measures the **Recovery Time Objective (RTO)**—the time taken to restore business operations from immutable backups.

**Key Engineering Concepts Demonstrated:**
*   **Purple Teaming:** Integrated Attack (Red Team) and Defense (Blue Team) logic.
*   **Operational Safety:** Strict sandbox confinement to prevent accidental system damage.
*   **Forensics:** Real-time file analysis and encryption verification.
*   **Metrics-Driven Security:** Automated calculation and visualization of RTO.

---

## 🏗️ System Architecture

The application follows a modular architecture separating the User Interface, Attack Logic, Defense Logic, and Safety Controls.

```mermaid
graph TD
    User[User / Admin] -->|Interacts| UI[Streamlit Dashboard]
    
    subgraph "Core Logic"
        UI -->|Trigger Attack| Villain[Villain (Attacker)]
        UI -->|Trigger Restore| Hero[Hero (Defender)]
        UI -->|View Metrics| Analyst[Analyst (Logger)]
    end
    
    subgraph "Safety Layer"
        Villain -->|Validate Path| Safety[Safety Enforcer]
        Hero -->|Validate Path| Safety
    end
    
    subgraph "File System Sandbox"
        Safety -->|Encrypts| Prod[./production_data]
        Safety -->|Restores from| Backup[./secure_backups]
    end
    
    Analyst -->|Reads/Writes| Logs[incident_log.json]
```

---

## 🚀 Features

### 🔴 Red Team (The Villain)
*   **AES-128 Encryption:** Uses `cryptography.fernet` to cryptographically lock files.
*   **Ransom Note Generation:** Drops a realistic `READ_ME_TO_DECRYPT.txt` with a unique Incident ID.
*   **Targeted Attacks:** Specifically targets business file extensions (`.txt`, `.csv`, `.xlsx`, etc.).

### 🟢 Blue Team (The Hero)
*   **Immutable Restoration:** Wipes the infected environment and restores clean data from the secure backup source.
*   **Incident Closure:** Links the restoration event to the specific Incident ID for accurate reporting.

### 📊 The Analyst (Dashboard)
*   **Real-Time RTO Tracking:** Calculates the exact seconds between infection and recovery.
*   **Forensic Inspector:** Allows users to view file contents to verify encryption (gibberish) vs. clean text.
*   **Trend Analysis:** Plotly charts showing resilience improvements over time.

---

## 🛠️ Installation & Usage

### Prerequisites
*   Python 3.9 or higher

### 1. Setup
```bash
# Clone the repository (if applicable) or navigate to folder
cd ransomware_rto_dashboard

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Dashboard
```bash
streamlit run app.py
```

### 3. The Demo Flow (How to present this)
1.  **Verify Health:** Show the "System Health" metric is **Secure**.
2.  **Inspect Data:** Use the "File Content Inspector" to read a dummy file (e.g., `client_list_1.txt`). Confirm it is readable.
3.  **Attack:** Click **"Simulate Ransomware Attack"**.
    *   Observe the progress bar.
    *   See the status change to **CRITICAL**.
    *   Read the **Ransom Note** popup.
    *   Inspect the file again—it is now encrypted binary data.
4.  **Recover:** Click **"Initiate Disaster Recovery"**.
    *   Watch the restoration progress.
    *   See the **Last RTO** metric update (e.g., "2.45s").
    *   Verify the file is readable again.

---

## 🔒 Safety Mechanisms

This tool includes a robust `SafetyEnforcer` module (`utils/safety.py`) to prevent accidental damage to your actual computer.

*   **Sandbox Confinement:** All file operations are strictly limited to `production_data` and `secure_backups`.
*   **Root Guard:** Explicitly blocks operations on system root directories (`/`, `C:\`, `/home`, etc.).
*   **Path Validation:** Uses `pathlib` resolution to prevent directory traversal attacks.

---

## 📂 Project Structure

```text
ransomware_rto_dashboard/
├── app.py                 # Main Streamlit Application
├── requirements.txt       # Project Dependencies
├── production_data/       # The "Target" (Sandboxed environment)
├── secure_backups/        # The "Source" (Immutable backups)
├── incident_log.json      # Audit log of all drills
└── utils/
    ├── config.py          # Centralized configuration
    ├── safety.py          # Safety enforcement logic
    ├── villain.py         # Attack logic
    ├── hero.py            # Recovery logic
    └── analyst.py         # Metrics and logging
```

---

## ⚠️ Disclaimer

**EDUCATIONAL USE ONLY.**
This software contains code that encrypts files. While strict safety measures are implemented, the author is not responsible for any data loss or misuse. Always run this in the provided isolated environment.
