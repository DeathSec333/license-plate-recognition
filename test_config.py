from src.config import Config

config = Config()
print("Application name:", config.get("application", "name"))
print("Detection threshold:", config.get("detection", "confidence_threshold"))
print("Database path:", config.get("database", "path"))
