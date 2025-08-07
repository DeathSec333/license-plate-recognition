#!/usr/bin/env python3
"""
Interactive License Plate Scanner
"""
import cv2
import os
import sys
from src.plate_detector import PlateDetector
from src.advanced_detector import AdvancedPlateDetector
from src.cascade_detector import CascadeDetector
from src.yolo_detector import YOLODetector
from src.ocr_engine import OCREngine

class LicensePlateScanner:
    def __init__(self):
        self.detectors = {
            '1': ('Basic Edge Detection', PlateDetector()),
            '2': ('Advanced Morphological', AdvancedPlateDetector()),
            '3': ('Cascade Detection', CascadeDetector()),
            '4': ('Template Matching', YOLODetector()),
            '5': ('All Methods', 'all')
        }
        self.ocr = OCREngine()
    
    def display_menu(self):
        print("\n" + "="*50)
        print("    LICENSE PLATE RECOGNITION SYSTEM")
        print("="*50)
        print("Detection Methods:")
        for key, (name, _) in self.detectors.items():
            print(f"  {key}. {name}")
        print("  0. Exit")
        print("-"*50)
    
    def get_image_path(self):
        while True:
            path = input("\nEnter image path (or 'back' to return): ").strip()
            
            if path.lower() == 'back':
                return None
            
            if path.startswith('"') and path.endswith('"'):
                path = path[1:-1]  # Remove quotes
            
            if os.path.exists(path):
                return path
            else:
                print(f"❌ File not found: {path}")
                print("Please check the path and try again.")
    
    def scan_with_method(self, image, method_key):
        if method_key == '5':  # All methods
            results = []
            for key in ['1', '2', '3', '4']:
                name, detector = self.detectors[key]
                plates = detector.detect_plates(image)
                results.append((name, plates))
            return results
        else:
            name, detector = self.detectors[method_key]
            plates = detector.detect_plates(image)
            return [(name, plates)]
    
    def process_image(self, image_path, method_key):
        print(f"\n🔍 Processing: {os.path.basename(image_path)}")
        print("-"*40)
        
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            print("❌ Error: Could not load image")
            return
        
        print(f"📷 Image loaded: {image.shape[1]}x{image.shape[0]} pixels")
        
        # Scan with selected method(s)
        results = self.scan_with_method(image, method_key)
        
        total_plates = 0
        for method_name, plates in results:
            print(f"\n🔎 {method_name}:")
            print(f"   Found {len(plates)} potential plates")
            
            for i, plate in enumerate(plates):
                total_plates += 1
                print(f"   📋 Plate {i+1}: Size {plate.shape}")
                
                # OCR processing
                try:
                    text = self.ocr.extract_text(plate)
                    if text.strip():
                        print(f"   📝 OCR Result: '{text.strip()}'")
                    else:
                        print("   📝 OCR Result: No text detected")
                except Exception as e:
                    print(f"   ❌ OCR Error: {e}")
        
        if total_plates == 0:
            print("\n❌ No license plates detected in this image")
            print("💡 Try a different detection method or check image quality")
        else:
            print(f"\n✅ Scan complete! Found {total_plates} total detections")
    
    def run(self):
        print("Welcome to License Plate Recognition System!")
        
        while True:
            self.display_menu()
            
            choice = input("\nSelect detection method (0-5): ").strip()
            
            if choice == '0':
                print("👋 Goodbye!")
                break
            
            if choice not in self.detectors:
                print("❌ Invalid choice. Please select 0-5.")
                continue
            
            # Get image path
            image_path = self.get_image_path()
            if image_path is None:
                continue
            
            # Process the image
            self.process_image(image_path, choice)
            
            # Ask if user wants to continue
            while True:
                continue_choice = input("\nScan another image? (y/n): ").strip().lower()
                if continue_choice in ['y', 'yes']:
                    break
                elif continue_choice in ['n', 'no']:
                    print("👋 Goodbye!")
                    return
                else:
                    print("Please enter 'y' or 'n'")

if __name__ == "__main__":
    scanner = LicensePlateScanner()
    scanner.run()
