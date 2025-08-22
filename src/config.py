import os
import yaml
from pathlib import Path

class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Load configuration from YAML file."""
        config_path = Path(os.path.dirname(os.path.dirname(__file__))) / "config.yml"
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
            
        with open(config_path, 'r') as file:
            self._config = yaml.safe_load(file)
    
    def get(self, section, key=None):
        """Get configuration value."""
        if section not in self._config:
            return None
            
        if key is None:
            return self._config[section]
            
        return self._config[section].get(key)
    
    def reload(self):
        """Reload configuration from file."""
        self._load_config()
        return self
