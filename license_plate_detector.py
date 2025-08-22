from src.config import Config

class LicensePlateDetector:
    def __init__(self):
        config = Config()
        self.confidence_threshold = config.get("detection", "confidence_threshold")
        self.max_detections = config.get("detection", "max_detections")
        self.model_path = config.get("detection", "model_path")
        # Rest of your initialization code
