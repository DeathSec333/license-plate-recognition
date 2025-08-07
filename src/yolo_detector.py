import cv2
import numpy as np

class YOLODetector:
    def __init__(self):
        # This would require YOLO weights trained on license plates
        # For now, implementing a template matching approach
        pass
    
    def detect_plates(self, image):
        """Template matching for license plate detection"""
        plates = []
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Create multiple templates for different plate sizes
        templates = self.create_plate_templates()
        
        for template in templates:
            # Template matching
            result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
            locations = np.where(result >= 0.6)
            
            for pt in zip(*locations[::-1]):
                x, y = pt
                w, h = template.shape[::-1]
                plate_roi = image[y:y+h, x:x+w]
                plates.append(plate_roi)
        
        return plates
    
    def create_plate_templates(self):
        """Create basic rectangular templates"""
        templates = []
        
        # Different plate sizes (width, height)
        sizes = [(120, 30), (100, 25), (140, 35)]
        
        for w, h in sizes:
            template = np.ones((h, w), dtype=np.uint8) * 255
            # Add border to simulate plate edge
            cv2.rectangle(template, (2, 2), (w-3, h-3), 0, 2)
            templates.append(template)
        
        return templates
