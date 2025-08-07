#!/usr/bin/env python3
import cv2
import numpy as np
from src.plate_detector import PlateDetector
from src.advanced_detector import AdvancedPlateDetector
from src.cascade_detector import CascadeDetector

def test_all_detectors():
    # Create a simple test image
    test_image = np.ones((300, 600, 3), dtype=np.uint8) * 128
    
    # Add a rectangle to simulate a license plate
    cv2.rectangle(test_image, (200, 120), (400, 180), (255, 255, 255), -1)
    cv2.rectangle(test_image, (200, 120), (400, 180), (0, 0, 0), 2)
    
    print("Testing all detectors...")
    
    # Test basic detector
    detector1 = PlateDetector()
    plates1 = detector1.detect_plates(test_image)
    print(f"Basic detector found {len(plates1)} plates")
    
    # Test advanced detector
    detector2 = AdvancedPlateDetector()
    plates2 = detector2.detect_plates(test_image)
    print(f"Advanced detector found {len(plates2)} plates")
    
    # Test cascade detector
    detector3 = CascadeDetector()
    plates3 = detector3.detect_plates(test_image)
    print(f"Cascade detector found {len(plates3)} plates")
    
    print("All detectors tested successfully!")

if __name__ == "__main__":
    test_all_detectors()
