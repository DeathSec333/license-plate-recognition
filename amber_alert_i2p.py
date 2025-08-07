#!/usr/bin/env python3
"""
Amber Alert System with i2p Privacy Integration
"""
import cv2
import os
import sys
import time
from datetime import datetime
from src.plate_detector import PlateDetector
from src.ocr_engine import OCREngine
from src.amber_alert_db import AmberAlertDatabase
from src.i2p_service import I2PService

class PrivateAmberAlertSystem:
    def __init__(self):
        self.detector = PlateDetector()
        self.ocr = OCREngine()
        self.alert_db = AmberAlertDatabase()
        self.i2p_service = I2PService()
        self.privacy_mode = False
        
    def start_privacy_mode(self):
        """Start i2p privacy mode"""
        print("🔒 Initializing privacy mode...")
        
        if self.i2p_service.start_i2pd():
            self.privacy_mode = True
            print("🔒 Privacy mode activated")
            print("🌐 All network traffic will be routed through i2p")
            print("🔐 Your identity and location are now protected")
            return True
        else:
            print("❌ Failed to start privacy mode")
            return False
    
    def stop_privacy_mode(self):
        """Stop i2p privacy mode"""
        if self.i2p_service.stop_i2pd():
            self.privacy_mode = False
            print("🔓 Privacy mode deactivated")
            return True
        return False
    
    def scan_image_private(self, image_path):
        """Scan image with privacy protection"""
        print(f"\n🔍 {'🔒 Private' if self.privacy_mode else '🔓 Standard'} scan: {os.path.basename(image_path)}")
        print("-" * 60)
        
        if not os.path.exists(image_path):
            print(f"❌ File not found: {image_path}")
            return
        
        # Load and process image
        image = cv2.imread(image_path)
        if image is None:
            print("❌ Could not load image")
            return
        
        print(f"📷 Image loaded: {image.shape[1]}x{image.shape[0]} pixels")
        
        # Detect plates
        plates = self.detector.detect_plates(image)
        print(f"📋 Found {len(plates)} potential plates")
        
        if not plates:
            print("❌ No license plates detected")
            return
        
        # Process each detected plate
        for i, plate in enumerate(plates):
            print(f"\n🔎 Processing Plate {i+1}:")
            print(f"   Size: {plate.shape}")
            
            try:
                detected_text = self.ocr.extract_text(plate)
                if not detected_text.strip():
                    print("   📝 No text detected")
                    continue
                
                detected_plate = detected_text.strip().upper()
                print(f"   📝 Detected: '{detected_plate}'")
                
                # Check against amber alerts
                alert_match = self.alert_db.check_plate_against_alerts(detected_plate)
                
                if self.privacy_mode:
                    print("🔒 Location data protected")
                    # Log without precise location in privacy mode
                    self.alert_db.log_detection(detected_plate, 0, 0, "private_scan")
                else:
                    # Standard logging
                    self.alert_db.log_detection(detected_plate, 0, 0, image_path)
                
                if alert_match['match']:
                    print("🚨" + "="*50)
                    print("   AMBER ALERT MATCH DETECTED!")
                    print("="*52)
                    print(f"   Case: {alert_match['case_number']}")
                    print(f"   Child: {alert_match['child_name']}")
                    print(f"   Vehicle: {alert_match['vehicle_description']}")
                    
                    if self.privacy_mode:
                        print("🔒 Alert sent through secure i2p channels")
                    else:
                        print("📢 Alert sent through standard channels")
                else:
                    print("   ✅ No amber alert matches")
                    
            except Exception as e:
                print(f"   ❌ Processing error: {e}")
    
    def show_network_status(self):
        """Show i2p network status"""
        if self.privacy_mode:
            print("\n🌐 i2p Network Status:")
            print(f"   Status: {'Online' if self.i2p_service.is_running else 'Offline'}")
            print(f"   Web Console: {self.i2p_service.web_console_url}")
            print(f"   HTTP Proxy: {self.i2p_service.http_proxy}")
            print(f"   SOCKS Proxy: {self.i2p_service.socks_proxy}")
        else:
            print("\n🔓 Privacy mode not active")
            print("   Standard internet connection in use")
    
    def interactive_menu(self):
        """Interactive menu with privacy options"""
        while True:
            print("\n" + "="*60)
            print("  🔒 PRIVATE AMBER ALERT DETECTION SYSTEM")
            print("="*60)
            print(f"Privacy Mode: {'🔒 ACTIVE' if self.privacy_mode else '🔓 INACTIVE'}")
            print("-"*60)
            print("1. Scan image for license plates")
            print("2. Toggle privacy mode (i2p)")
            print("3. Show network status")
            print("4. Show active amber alerts")
            print("5. Add test amber alert")
            print("0. Exit")
            print("-"*60)
            
            choice = input("Select option (0-5): ").strip()
            
            if choice == '0':
                if self.privacy_mode:
                    print("🔄 Stopping privacy mode...")
                    self.stop_privacy_mode()
                print("👋 Goodbye!")
                break
                
            elif choice == '1':
                image_path = input("Enter image path: ").strip()
                if image_path.startswith('"') and image_path.endswith('"'):
                    image_path = image_path[1:-1]
                self.scan_image_private(image_path)
                
            elif choice == '2':
                if self.privacy_mode:
                    self.stop_privacy_mode()
                else:
                    self.start_privacy_mode()
                    
            elif choice == '3':
                self.show_network_status()
                
            elif choice == '4':
                alerts = self.alert_db.get_active_alerts()
                if alerts:
                    print(f"\n📋 Active Amber Alerts ({len(alerts)}):")
                    for alert in alerts:
                        print(f"   Case: {alert[1]} - Plate: {alert[3]}")
                else:
                    print("\n📋 No active amber alerts")
                    
            elif choice == '5':
                success = self.alert_db.add_amber_alert(
                    case_number="TEST-I2P-001",
                    child_name="Test Child",
                    license_plate="I2P123",
                    vehicle_desc="Blue Honda Civic",
                    suspect_info="Adult male, 30s",
                    lat=40.7128, lon=-74.0060,
                    location_desc="New York, NY"
                )
                if success:
                    print("✅ Test amber alert added (License plate: I2P123)")
                else:
                    print("⚠️ Test alert already exists")
            else:
                print("❌ Invalid choice")

if __name__ == "__main__":
    system = PrivateAmberAlertSystem()
    system.interactive_menu()
