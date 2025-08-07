import cv2
import numpy as np

class CascadeDetector:
    def __init__(self):
        # You can download haarcascade_licence_plate_rus_16stages.xml
        # or train your own cascade classifier
        self.cascade_path = 'haarcascade_russian_plate_number.xml'
        try:
            self.plate_cascade = cv2.CascadeClassifier(self.cascade_path)
        except:
            print("Cascade file not found, using contour method as fallback")
            self.plate_cascade = None
    
    def detect_plates(self, image):
        """Detect plates using Haar cascade classifier"""
        plates = []
        
        if self.plate_cascade is None:
            return self.fallback_detection(image)
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect plates
        detected_plates = self.plate_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30)
        )
        
        for (x, y, w, h) in detected_plates:
            plate_roi = image[y:y+h, x:x+w]
            plates.append(plate_roi)
        
        return plates
    
    def fallback_detection(self, image):
        """Fallback method using basic contour detection"""
        # Simple contour-based detection as backup
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        plates = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            area = cv2.contourArea(contour)
            
            if 2.0 <= aspect_ratio <= 5.0 and area > 1000:
                plate_roi = image[y:y+h, x:x+w]
                plates.append(plate_roi)
        
        return plates
