from src.config import Config
import cv2
import numpy as np
import pytesseract
from datetime import datetime

class PlateScan:
    def __init__(self):
        config = Config()
        self.image_width = config.get("image", "width")
        self.image_height = config.get("image", "height")
        self.supported_formats = config.get("image", "formats")
        self.log_file = config.get("logging", "file")
        self.log_level = config.get("logging", "level")
        
    def scan(self, image_path):
        # Your existing scan code here
        # Replace hardcoded values with self.image_width, self.image_height, etc.
        pass
        
    def process_results(self, plate_text):
        # Your existing processing code here
        pass
        
# Your existing code below this line
