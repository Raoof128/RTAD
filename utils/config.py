from pathlib import Path

class Config:
    """
    Centralized configuration for the Ransomware RTO Dashboard.
    """
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # Directories
    PRODUCTION_DIR = BASE_DIR / "production_data"
    BACKUP_DIR = BASE_DIR / "secure_backups"
    
    # Files
    LOG_FILE = BASE_DIR / "incident_log.json"
    KEY_FILE = BASE_DIR / "ransomware.key"
    RANSOM_NOTE_FILE = "READ_ME_TO_DECRYPT.txt"
    
    # Extensions to target
    TARGET_EXTENSIONS = ('.txt', '.csv', '.xlsx', '.docx', '.json', '.md', '.log')
    
    # System Critical Paths (Blocklist)
    # Note: We exclude /home because in many CI/CD environments (like GitHub Actions), 
    # the runner operates inside /home/runner, so blocking /home blocks the project itself.
    CRITICAL_PATHS = [Path("/"), Path("/root"), Path("/etc"), Path("/var"), Path("/bin"), Path("/usr")]
