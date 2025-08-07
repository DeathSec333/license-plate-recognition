import pytesseract
import cv2

class OCREngine:
    def __init__(self):
        # Set tesseract path for Termux
        pytesseract.pytesseract.tesseract_cmd = '/data/data/com.termux/files/usr/bin/tesseract'
    
    def extract_text(self, plate_image):
        """Extract text from plate image"""
        # Convert BGR to RGB if needed
        if len(plate_image.shape) == 3:
            plate_image = cv2.cvtColor(plate_image, cv2.COLOR_BGR2RGB)
        
        # Use specific config for license plates
        config = '--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        text = pytesseract.image_to_string(plate_image, config=config)
        return text.strip()
