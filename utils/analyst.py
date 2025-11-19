import pandas as pd
from datetime import datetime
import json
import os
from pathlib import Path
from .config import Config

class Analyst:
    """
    The Analyst acts as the logging and metrics engine.
    It tracks RTO (Recovery Time Objective) which is a critical metric in 
    ISO 22301 (Business Continuity) and ISO 27001.
    """
    
    @staticmethod
    def log_event(event_type, details=None, incident_id=None):
        """
        Logs an event with a timestamp and optional incident ID.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "incident_id": incident_id,
            "details": details or {}
        }
        
        logs = Analyst.get_logs()
        logs.append(entry)
        
        with open(Config.LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

    @staticmethod
    def get_logs():
        if not Config.LOG_FILE.exists():
            return []
        try:
            with open(Config.LOG_FILE, "r") as f:
                return json.load(f)
        except:
            return []

    @staticmethod
    def calculate_last_rto():
        """
        Calculates the RTO of the most recently completed recovery cycle.
        Returns tuple: (seconds, incident_id)
        """
        logs = Analyst.get_logs()
        if not logs:
            return None, None
            
        # Find last restore complete
        last_restore = None
        for log in reversed(logs):
            if log["event"] == "Restore Complete":
                last_restore = log
                break
        
        if not last_restore:
            return None, None
            
        # Find corresponding attack start with the same incident_id
        incident_id = last_restore.get("incident_id")
        last_attack = None
        
        if incident_id:
            # Precise matching
            for log in reversed(logs):
                if log["event"] == "Attack Start" and log.get("incident_id") == incident_id:
                    last_attack = log
                    break
        else:
            # Fallback for legacy logs without IDs
            restore_time = datetime.fromisoformat(last_restore["timestamp"])
            for log in reversed(logs):
                log_time = datetime.fromisoformat(log["timestamp"])
                if log["event"] == "Attack Start" and log_time < restore_time:
                    last_attack = log
                    break
                
        if last_attack and last_restore:
            start = datetime.fromisoformat(last_attack["timestamp"])
            end = datetime.fromisoformat(last_restore["timestamp"])
            return (end - start).total_seconds(), incident_id
            
        return None, None

    @staticmethod
    def get_rto_history():
        """Returns a list of RTO records for plotting."""
        logs = Analyst.get_logs()
        history = []
        
        # Group by incident ID or simple chronological pairing
        # We'll do a simple pass: find Restore, find matching Attack
        restores = [l for l in logs if l["event"] == "Restore Complete"]
        
        for restore in restores:
            r_time = datetime.fromisoformat(restore["timestamp"])
            incident_id = restore.get("incident_id")
            
            attack = None
            if incident_id:
                for l in logs:
                    if l["event"] == "Attack Start" and l.get("incident_id") == incident_id:
                        attack = l
                        break
            else:
                # Fallback: find closest attack before this restore
                candidates = [l for l in logs if l["event"] == "Attack Start" and datetime.fromisoformat(l["timestamp"]) < r_time]
                if candidates:
                    attack = candidates[-1]
            
            if attack:
                a_time = datetime.fromisoformat(attack["timestamp"])
                rto = (r_time - a_time).total_seconds()
                history.append({
                    "incident_id": incident_id or "legacy",
                    "date": r_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "rto_seconds": rto
                })
        return history
