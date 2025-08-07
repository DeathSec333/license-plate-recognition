import cv2
import numpy as np
import imutils

class PlateDetector:
    def __init__(self):
        self.min_area = 500
        self.max_area = 10000
        
    def detect_plates(self, image):
        """Multi-algorithm plate detection"""
        plates = []
        
        # Method 1: Edge detection + contours
        plates.extend(self.edge_detection_method(image))
        
        # Method 2: Morphological operations
        plates.extend(self.morphological_method(image))
        
        # Remove duplicates and return best candidates
        return self.filter_duplicates(plates)
    
    def edge_detection_method(self, image):
        """Edge detection approach"""
        plates = []
        image_resized = imutils.resize(image, width=500)
        gray = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
        
        # Bilateral filter + Canny edge detection
        filtered = cv2.bilateralFilter(gray, 11, 17, 17)
        edges = cv2.Canny(filtered, 30, 200)
        
        contours = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        
        for contour in contours:
            epsilon = 0.018 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            if len(approx) == 4:
                area = cv2.contourArea(contour)
                if self.min_area < area < self.max_area:
                    x, y, w, h = cv2.boundingRect(approx)
                    # Scale back to original image
                    scale = image.shape[1] / 500
                    x, y, w, h = int(x*scale), int(y*scale), int(w*scale), int(h*scale)
                    plate_roi = image[y:y+h, x:x+w]
                    if plate_roi.size > 0:
                        plates.append(plate_roi)
        
        return plates
    
    def morphological_method(self, image):
        """Morphological operations approach"""
        plates = []
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Morphological gradient
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        gradient = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
        
        # Threshold and close
        _, thresh = cv2.threshold(gradient, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 1000:
                continue
                
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            
            if 2.0 <= aspect_ratio <= 5.0:
                plate_roi = image[y:y+h, x:x+w]
                plates.append(plate_roi)
        
        return plates
    
    def filter_duplicates(self, plates):
        """Remove duplicate detections"""
        if not plates:
            return plates
        
        # Simple duplicate removal based on size similarity
        filtered = []
        for plate in plates:
            is_duplicate = False
            for existing in filtered:
                if abs(plate.shape[0] - existing.shape[0]) < 10 and \
                   abs(plate.shape[1] - existing.shape[1]) < 10:
                    is_duplicate = True
                    break
            if not is_duplicate:
                filtered.append(plate)
        
        return filtered[:3]  # Return top 3 candidates
