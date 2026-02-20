import json
import os

def load_config(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    
    return config

def get_db_config():
    config_path = os.path.join(os.path.dirname(__file__), '../../config/db_config.json')
    return load_config(config_path)