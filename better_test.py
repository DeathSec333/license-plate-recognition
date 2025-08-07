#!/usr/bin/env python3
import cv2
import numpy as np
from src.plate_detector import PlateDetector
from src.advanced_detector import AdvancedPlateDetector
from src.cascade_detector import CascadeDetector
from src.yolo_detector import YOLODetector
from src.ocr_engine import OCREngine

def create_realistic_test_image():
    """Create a more realistic test image"""
    # Create background with some noise
    img = np.random.randint(100, 150, (400, 800, 3), dtype=np.uint8)
    
    # Add a realistic license plate
    plate_x, plate_y = 250, 150
    plate_w, plate_h = 300, 100
    
    # White plate background
    cv2.rectangle(img, (plate_x, plate_y), (plate_x + plate_w, plate_y + plate_h), (255, 255, 255), -1)
    
    # Black border
    cv2.rectangle(img, (plate_x, plate_y), (plate_x + plate_w, plate_y + plate_h), (0, 0, 0), 3)
    
    # Add some text-like shapes
    text_y = plate_y + 30
    text_positions = [270, 310, 350, 390, 430, 470, 510]
    
    for i, x in enumerate(text_positions):
        # Create letter/number-like rectangles
        cv2.rectangle(img, (x, text_y), (x + 25, text_y + 40), (0, 0, 0), -1)
        # Add some variation
        if i % 2 == 0:
            cv2.rectangle(img, (x + 5, text_y + 10), (x + 20, text_y + 30), (255, 255, 255), -1)
    
    return img

def test_with_better_image():
    print("=== Better License Plate Detection Test ===\n")
    
    # Create realistic test image
    img = create_realistic_test_image()
    print("Created realistic test image with license plate")
    
    # Save test image for inspection
    cv2.imwrite('test_image.jpg', img)
    print("Saved test image as 'test_image.jpg'")
    
    # Test each detector
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
            print(f"\n{name:12}: {len(plates):2d} plates detected")
            
            # Test OCR on first plate only
            if plates and len(plates) > 0:
                print(f"             Size: {plates[0].shape}")
                try:
                    text = ocr.extract_text(plates[0])
                    if text.strip():
                        print(f"             OCR: '{text.strip()}'")
                    else:
                        print("             OCR: No text detected")
                except Exception as e:
                    print(f"             OCR Error: {e}")
                    
        except Exception as e:
            print(f"{name:12}: Error - {e}")
    
    print("\n=== Test Complete ===")
    print("Check 'test_image.jpg' to see the test image")

if __name__ == "__main__":
    test_with_better_image()
