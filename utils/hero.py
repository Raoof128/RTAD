import os
import shutil
from pathlib import Path
from .safety import SafetyEnforcer
from .analyst import Analyst
from .config import Config
import time

class Hero:
    """
    The Hero performs Disaster Recovery (DR).
    It restores data from the immutable backup source, demonstrating 'Resilience'.
    """

    @staticmethod
    def restore_operations(progress_callback=None):
        """
        Wipes the infected production folder and restores from backups.
        """
        SafetyEnforcer.ensure_directories()
        
        # Get current active incident to close the loop
        current_incident_id = Analyst.get_current_incident_id()
        Analyst.log_event("Restore Start", incident_id=current_incident_id)
        
        prod_dir = Config.PRODUCTION_DIR
        backup_dir = Config.BACKUP_DIR
        
        # 1. Wipe Production (Simulate cleaning infected host)
        # We'll count items to wipe for progress estimation
        items_to_wipe = list(prod_dir.iterdir())
        total_ops = len(items_to_wipe) + len(list(backup_dir.iterdir()))
        current_op = 0
        
        for item_path in items_to_wipe:
            if SafetyEnforcer.validate_path(item_path):
                try:
                    if item_path.is_file():
                        os.remove(item_path)
                    elif item_path.is_dir():
                        shutil.rmtree(item_path)
                except Exception as e:
                    print(f"Error wiping {item_path.name}: {e}")
            
            current_op += 1
            if progress_callback:
                progress_callback(current_op / total_ops if total_ops > 0 else 0)
        
        # 2. Restore from Backup
        restored_count = 0
        if backup_dir.exists():
            backup_items = list(backup_dir.iterdir())
            for item in backup_items:
                s = backup_dir / item
                d = prod_dir / item
                
                # Safety check for source as well, just in case
                if not SafetyEnforcer.validate_path(s):
                    continue

                try:
                    if s.is_file():
                        shutil.copy2(s, d)
                        restored_count += 1
                    elif s.is_dir():
                        shutil.copytree(s, d)
                        restored_count += 1
                except Exception as e:
                    print(f"Error restoring {item.name}: {e}")
                
                current_op += 1
                if progress_callback:
                    progress_callback(current_op / total_ops if total_ops > 0 else 0)
                
                # Artificial delay for dramatic effect
                time.sleep(0.05)
        
        Analyst.log_event("Restore Complete", {"files_restored": restored_count}, incident_id=current_incident_id)
        return restored_count

    @staticmethod
    def generate_dummy_data():
        """
        Generates dummy data in the backup folder and syncs to production
        to initialize the simulation.
        """
        SafetyEnforcer.ensure_directories()
        backup_dir = Config.BACKUP_DIR
        
        # Create some dummy files if empty
        if not any(backup_dir.iterdir()):
            for i in range(1, 6):
                with open(backup_dir / f"financial_record_{i}.csv", "w") as f:
                    f.write("id,amount,status\n1,100,paid\n2,200,pending")
                with open(backup_dir / f"client_list_{i}.txt", "w") as f:
                    f.write(f"Confidential Client Data {i} - Do Not Leak")
                with open(backup_dir / f"project_plan_{i}.md", "w") as f:
                    f.write(f"# Project Alpha {i}\n\n## Confidential\nThis is a top secret project.")
            
            # Sync to production
            Hero.restore_operations()
