from src.config import Config
import os

def test_config_integration():
    config = Config()
    
    # Test that config values are accessible
    print("Testing configuration access:")
    print(f"Application: {config.get('application', 'name')} v{config.get('application', 'version')}")
    print(f"Image dimensions: {config.get('image', 'width')}x{config.get('image', 'height')}")
    print(f"Database: {config.get('database', 'path')}")
    
    # Test that config file exists
    config_path = os.path.join(os.path.dirname(__file__), "config.yml")
    print(f"\nConfig file exists: {os.path.exists(config_path)}")
    
    print("\nConfiguration system is ready!")

if __name__ == "__main__":
    test_config_integration()
