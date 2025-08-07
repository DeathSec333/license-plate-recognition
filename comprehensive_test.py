#!/usr/bin/env python3
import cv2
import numpy as np
from src.plate_detector import PlateDetector
from src.advanced_detector import AdvancedPlateDetector
from src.cascade_detector import CascadeDetector
from src.yolo_detector import YOLODetector
from src.ocr_engine import OCREngine

def create_test_image_with_text():
    """Create a test image with simulated license plate"""
    # Create white background
    img = np.ones((400, 800, 3), dtype=np.uint8) * 200
    
    # Add license plate background
    cv2.rectangle(img, (250, 150), (550, 250), (255, 255, 255), -1)
    cv2.rectangle(img, (250, 150), (550, 250), (0, 0, 0), 3)
    
    # Add some text-like rectangles
    cv2.rectangle(img, (270, 180), (290, 220), (0, 0, 0), -1)  # A
    cv2.rectangle(img, (300, 180), (320, 220), (0, 0, 0), -1)  # B
    cv2.rectangle(img, (330, 180), (350, 220), (0, 0, 0), -1)  # C
    cv2.rectangle(img, (370, 180), (390, 220), (0, 0, 0), -1)  # 1
    cv2.rectangle(img, (400, 180), (420, 220), (0, 0, 0), -1)  # 2
    cv2.rectangle(img, (430, 180), (450, 220), (0, 0, 0), -1)  # 3
    
    return img

def test_all_detectors_comprehensive():
    print("=== Comprehensive License Plate Detection Test ===\n")
    
    # Create test image
    test_image = create_test_image_with_text()
    print("Created test image with simulated license plate")
    
    # Initialize OCR
    ocr = OCREngine()
    
    detectors = [
        ("Basic Edge Detection", PlateDetector()),
        ("Advanced Morphological", AdvancedPlateDetector()),
        ("Cascade (with fallback)", CascadeDetector()),
        ("Template Matching", YOLODetector())
    ]
    
    for name, detector in detectors:
        print(f"\n--- Testing {name} ---")
        try:
            plates = detector.detect_plates(test_image)
            print(f"Detected {len(plates)} potential plates")
            
            for i, plate in enumerate(plates):
                if plate.size > 0:
                    print(f"  Plate {i+1}: Size {plate.shape}")
                    # Try OCR on detected plate
                    try:
                        text = ocr.extract_text(plate)
                        if text.strip():
                            print(f"    OCR Result: '{text.strip()}'")
                        else:
                            print("    OCR Result: No text detected")
                    except Exception as e:
                        print(f"    OCR Error: {e}")
                        
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_all_detectors_comprehensive()
