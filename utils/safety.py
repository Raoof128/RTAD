from pathlib import Path
from .config import Config

class SafetyEnforcer:
    """
    Ensures all file operations are restricted to the designated sandbox directories.
    This aligns with ISO 27001 operational security controls to prevent accidental damage.
    """
    
    @staticmethod
    def validate_path(target_path: Path) -> bool:
        """
        Validates that the target path is strictly within the allowed sandbox directories.
        Uses robust path resolution to prevent directory traversal attacks.
        """
        try:
            resolved_path = target_path.resolve()
            prod_dir = Config.PRODUCTION_DIR.resolve()
            backup_dir = Config.BACKUP_DIR.resolve()
            
            # Critical: Prevent operations on system root or critical paths
            for p in Config.CRITICAL_PATHS:
                # If the critical path is root, only block if it IS root (don't block children of root, which is everything)
                if str(p) == "/":
                    if resolved_path == p:
                        return False
                # For other critical paths (e.g. /etc), block the path and any children
                else:
                    if resolved_path == p or p in resolved_path.parents:
                        return False

            # Check if path is relative to (inside) the allowed directories
            is_in_prod = False
            try:
                resolved_path.relative_to(prod_dir)
                is_in_prod = True
            except ValueError:
                pass

            is_in_backup = False
            try:
                resolved_path.relative_to(backup_dir)
                is_in_backup = True
            except ValueError:
                pass
            
            return is_in_prod or is_in_backup
        except Exception as e:
            print(f"Safety Check Error: {e}")
            return False

    @staticmethod
    def ensure_directories():
        """Creates necessary directories if they don't exist."""
        Config.PRODUCTION_DIR.mkdir(parents=True, exist_ok=True)
        Config.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
