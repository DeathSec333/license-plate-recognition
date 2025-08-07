#!/usr/bin/env python3
import cv2
import numpy as np
from src.plate_detector import PlateDetector
from src.advanced_detector import AdvancedPlateDetector
from src.cascade_detector import CascadeDetector
from src.yolo_detector import YOLODetector
from src.ocr_engine import OCREngine

def quick_test():
    print("=== Quick License Plate Detection Test ===\n")
    
    # Create simple test image
    img = np.ones((300, 600, 3), dtype=np.uint8) * 200
    cv2.rectangle(img, (200, 100), (400, 200), (255, 255, 255), -1)
    cv2.rectangle(img, (200, 100), (400, 200), (0, 0, 0), 3)
    
    # Test each detector with limited output
    detectors = [
        ("Basic", PlateDetector()),
        ("Advanced", AdvancedPlateDetector()),
        ("Cascade", CascadeDetector()),
        ("Template", YOLODetector())
    ]
    
    ocr = OCREngine()
    
    for name, detector in detectors:
        try:
            plates = detector.detect_plates(img)
            print(f"{name:12}: {len(plates):2d} plates detected")
            
            # Test OCR on first plate only
            if plates and len(plates) > 0:
                text = ocr.extract_text(plates[0])
                if text.strip():
                    print(f"             OCR: '{text.strip()}'")
                    
        except Exception as e:
            print(f"{name:12}: Error - {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    quick_test()
