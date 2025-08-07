import sqlite3
import json
from datetime import datetime, timedelta

class AmberAlertDatabase:
    def __init__(self, db_path="amber_alerts.db"):
        self.db_path = db_path
        self.setup_database()
    
    def setup_database(self):
        """Initialize the amber alert database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Amber alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS amber_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_number TEXT UNIQUE,
                child_name TEXT,
                license_plate TEXT,
                vehicle_description TEXT,
                suspect_info TEXT,
                location_lat REAL,
                location_lon REAL,
                last_seen_location TEXT,
                alert_timestamp TEXT,
                status TEXT DEFAULT 'ACTIVE',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Detection logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detection_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                detected_plate TEXT,
                detection_lat REAL,
                detection_lon REAL,
                detection_timestamp TEXT,
                image_path TEXT,
                confidence_score REAL,
                alert_match BOOLEAN DEFAULT FALSE,
                case_number TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_amber_alert(self, case_number, child_name, license_plate, 
                       vehicle_desc, suspect_info, lat, lon, location_desc):
        """Add new amber alert to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO amber_alerts 
                (case_number, child_name, license_plate, vehicle_description, 
                 suspect_info, location_lat, location_lon, last_seen_location, 
                 alert_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (case_number, child_name, license_plate.upper(), vehicle_desc, 
                  suspect_info, lat, lon, location_desc, datetime.now().isoformat()))
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def check_plate_against_alerts(self, detected_plate):
        """Check if detected plate matches any active amber alerts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM amber_alerts 
            WHERE license_plate = ? AND status = 'ACTIVE'
        ''', (detected_plate.upper(),))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'match': True,
                'case_number': result[1],
                'child_name': result[2],
                'vehicle_description': result[4],
                'suspect_info': result[5],
                'last_seen_lat': result[6],
                'last_seen_lon': result[7],
                'alert_timestamp': result[9]
            }
        return {'match': False}
    
    def log_detection(self, plate, lat, lon, image_path, confidence=0.0):
        """Log plate detection with location"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check for amber alert match
        alert_match = self.check_plate_against_alerts(plate)
        
        cursor.execute('''
            INSERT INTO detection_logs 
            (detected_plate, detection_lat, detection_lon, detection_timestamp,
             image_path, confidence_score, alert_match, case_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (plate.upper(), lat, lon, datetime.now().isoformat(),
              image_path, confidence, alert_match['match'], 
              alert_match.get('case_number', None)))
        
        conn.commit()
        conn.close()
        
        return alert_match
    
    def get_active_alerts(self):
        """Get all active amber alerts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM amber_alerts WHERE status = "ACTIVE"')
        results = cursor.fetchall()
        conn.close()
        
        return results
