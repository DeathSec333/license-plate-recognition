import cv2
import numpy as np

class AdvancedPlateDetector:
    def __init__(self):
        self.min_aspect_ratio = 2.0
        self.max_aspect_ratio = 5.0
        self.min_area = 1000
        
    def detect_plates(self, image):
        """Advanced plate detection using morphological operations"""
        plates = []
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        
        # Blackhat operation to highlight dark regions
        blackhat = cv2.morphologyEx(blurred, cv2.MORPH_BLACKHAT, kernel)
        
        # Gradient operation to highlight edges
        gradient = cv2.morphologyEx(blurred, cv2.MORPH_GRADIENT, kernel)
        
        # Combine operations
        combined = cv2.add(blackhat, gradient)
        
        # Threshold
        _, thresh = cv2.threshold(combined, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Closing operation to connect text regions
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < self.min_area:
                continue
                
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            
            # Check if aspect ratio matches license plate
            if self.min_aspect_ratio <= aspect_ratio <= self.max_aspect_ratio:
                # Extract plate region
                plate_roi = image[y:y+h, x:x+w]
                plates.append(plate_roi)
        
        return plates
