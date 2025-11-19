import unittest
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.analyst import Analyst
from utils.config import Config

class TestAnalyst(unittest.TestCase):

    def setUp(self):
        # Use a temporary log file for testing
        self.original_log_file = Config.LOG_FILE
        Config.LOG_FILE = Path("test_incident_log.json")
        
        # Clear any existing test log
        if Config.LOG_FILE.exists():
            Config.LOG_FILE.unlink()

    def tearDown(self):
        # Restore original log file path
        if Config.LOG_FILE.exists():
            Config.LOG_FILE.unlink()
        Config.LOG_FILE = self.original_log_file

    def test_log_event(self):
        """Test that events are correctly written to the JSON log."""
        Analyst.log_event("Test Event", {"foo": "bar"}, incident_id="INC-123")
        
        self.assertTrue(Config.LOG_FILE.exists())
        with open(Config.LOG_FILE, "r") as f:
            logs = json.load(f)
            
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["event"], "Test Event")
        self.assertEqual(logs[0]["incident_id"], "INC-123")
        self.assertEqual(logs[0]["details"]["foo"], "bar")

    def test_calculate_rto(self):
        """Test the RTO calculation logic."""
        # Simulate an attack 10 seconds ago
        start_time = datetime.now() - timedelta(seconds=10)
        end_time = datetime.now()
        
        # Manually write logs to simulate a sequence
        logs = [
            {
                "timestamp": start_time.isoformat(),
                "event": "Attack Start",
                "incident_id": "INC-TEST",
                "details": {}
            },
            {
                "timestamp": end_time.isoformat(),
                "event": "Restore Complete",
                "incident_id": "INC-TEST",
                "details": {}
            }
        ]
        
        with open(Config.LOG_FILE, "w") as f:
            json.dump(logs, f)
            
        rto, incident_id = Analyst.calculate_last_rto()
        
        self.assertEqual(incident_id, "INC-TEST")
        # Allow small delta for float precision
        self.assertAlmostEqual(rto, 10.0, delta=0.1)

if __name__ == '__main__':
    unittest.main()
