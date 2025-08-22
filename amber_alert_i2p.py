#!/usr/bin/env python3
from src.config import Config
import sqlite3
import time
import sys
import os

class AmberAlertSystem:
    def __init__(self):
        config = Config()
        self.db_path = config.get("database", "path")
        self.backup_interval = config.get("database", "backup_interval")
        self.log_level = config.get("logging", "level")
        self.log_file = config.get("logging", "file")
        self.setup_database()
        
    def setup_database(self):
        # Connect to the database using the configured path
        conn = sqlite3.connect(self.db_path)
        # Your existing database setup code
        conn.close()
        
    def check_plate(self, plate_number):
        # Your existing plate checking code
        # Use self.db_path instead of hardcoded path
        pass
        
    def log_activity(self, message):
        # Log based on configured log level
        if self.log_level in ["DEBUG", "INFO"]:
            with open(self.log_file, "a") as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

# Your existing code below this line
