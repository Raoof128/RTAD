import unittest
from pathlib import Path
import sys
import os

# Add parent directory to path to import utils
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.safety import SafetyEnforcer
from utils.config import Config

class TestSafetyEnforcer(unittest.TestCase):

    def setUp(self):
        # Ensure directories exist for testing
        Config.PRODUCTION_DIR.mkdir(parents=True, exist_ok=True)
        Config.BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    def test_allowed_paths(self):
        """Test that paths inside the sandbox are allowed."""
        safe_prod = Config.PRODUCTION_DIR / "test_file.txt"
        safe_backup = Config.BACKUP_DIR / "backup_file.txt"
        
        # Create files to ensure resolve() works consistently
        safe_prod.touch()
        safe_backup.touch()
        
        try:
            self.assertTrue(SafetyEnforcer.validate_path(safe_prod))
            self.assertTrue(SafetyEnforcer.validate_path(safe_backup))
        finally:
            # Cleanup
            if safe_prod.exists(): safe_prod.unlink()
            if safe_backup.exists(): safe_backup.unlink()

    def test_blocked_paths(self):
        """Test that paths outside the sandbox are blocked."""
        unsafe_paths = [
            Path("/"),
            Path("/etc/passwd"),
            Path.home(),
            Config.BASE_DIR / "app.py", # Inside project but outside sandbox
            Path(".."),
        ]
        
        for p in unsafe_paths:
            self.assertFalse(SafetyEnforcer.validate_path(p), f"Failed to block: {p}")

    def test_traversal_attempt(self):
        """Test that directory traversal attempts are blocked."""
        # Try to go up from production dir
        traversal = Config.PRODUCTION_DIR / "../secret.txt"
        self.assertFalse(SafetyEnforcer.validate_path(traversal))

if __name__ == '__main__':
    unittest.main()
