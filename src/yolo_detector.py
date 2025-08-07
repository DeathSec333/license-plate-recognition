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
            # Template matching with higher threshold
            result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
            locations = np.where(result >= 0.8)  # Increased threshold from 0.6 to 0.8
            
            # Limit detections to avoid too many false positives
            points = list(zip(*locations[::-1]))
            if len(points) > 5:  # Limit to top 5 matches
                points = points[:5]
            
            for pt in points:
                x, y = pt
                w, h = template.shape[::-1]
                
                # Check if detection is reasonable size
                if w > 50 and h > 15:  # Minimum reasonable plate size
                    plate_roi = image[y:y+h, x:x+w]
                    if plate_roi.size > 0:
                        plates.append(plate_roi)
        
        # Remove duplicates and return max 3 plates
        return self.filter_duplicates(plates)[:3]
    
    def create_plate_templates(self):
        """Create basic rectangular templates"""
        templates = []
        
        # Different plate sizes (width, height) - more realistic sizes
        sizes = [(200, 50), (160, 40), (240, 60)]
        
        for w, h in sizes:
            template = np.ones((h, w), dtype=np.uint8) * 255
            # Add border to simulate plate edge
            cv2.rectangle(template, (5, 5), (w-6, h-6), 0, 3)
            templates.append(template)
        
        return templates
    
    def filter_duplicates(self, plates):
        """Remove overlapping detections"""
        if not plates:
            return plates
        
        filtered = []
        for plate in plates:
            is_duplicate = False
            for existing in filtered:
                # Check if plates are similar in size (likely duplicates)
                if abs(plate.shape[0] - existing.shape[0]) < 20 and \
                   abs(plate.shape[1] - existing.shape[1]) < 20:
                    is_duplicate = True
                    break
            if not is_duplicate:
                filtered.append(plate)
        
        return filtered
