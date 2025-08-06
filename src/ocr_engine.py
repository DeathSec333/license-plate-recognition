import pytesseract

class OCREngine:
    def __init__(self):
        pass
    
    def extract_text(self, plate_image):
        """Extract text from plate image"""
        # TODO: Implement OCR logic
        return pytesseract.image_to_string(plate_image)
