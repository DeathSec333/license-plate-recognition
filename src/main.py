#!/usr/bin/env python3
"""
License Plate Recognition Main Module
"""
import argparse
import cv2
from plate_detector import PlateDetector
from ocr_engine import OCREngine

def main():
    parser = argparse.ArgumentParser(description='License Plate Recognition')
    parser.add_argument('--image', required=True, help='Path to input image')
    args = parser.parse_args()
    
    # Load image
    image = cv2.imread(args.image)
    if image is None:
        print(f"Error: Could not load image {args.image}")
        return
    
    # Process image
    detector = PlateDetector()
    ocr = OCREngine()
    
    plates = detector.detect_plates(image)
    for plate in plates:
        text = ocr.extract_text(plate)
        print(f"Detected plate: {text}")

if __name__ == "__main__":
    main()
