#!/usr/bin/env python3
"""
License Plate Recognition Main Module
"""
import argparse
import cv2
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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
    
    print(f"Image loaded successfully: {image.shape}")
    
    # Process image
    detector = PlateDetector()
    ocr = OCREngine()
    
    plates = detector.detect_plates(image)
    if not plates:
        print("No plates detected, trying OCR on whole image...")
        text = ocr.extract_text(image)
        print(f"Detected text: {text}")
    else:
        for i, plate in enumerate(plates):
            text = ocr.extract_text(plate)
            print(f"Plate {i+1}: {text}")

if __name__ == "__main__":
    main()
