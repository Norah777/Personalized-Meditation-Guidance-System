#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Settings and configurations for the application.
"""

import os
from typing import Dict, Any, Optional

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# =============================================================================
# API Configuration for Different Model Types
# =============================================================================

# Text Model Configuration
TEXT_API_KEY = os.environ.get("TEXT_API_KEY")
TEXT_BASE_URL = os.environ.get("TEXT_BASE_URL", "https://api.deepseek.com")
TEXT_MODEL_NAME = os.environ.get("TEXT_MODEL_NAME", "deepseek-chat")

# Image Model API Settings  
IMAGE_API_KEY = os.environ.get("IMAGE_API_KEY")
IMAGE_BASE_URL = os.environ.get("IMAGE_BASE_URL", "https://api.openai.com")
IMAGE_MODEL_NAME = os.environ.get("IMAGE_MODEL_NAME", "dall-e-3")

# Text-to-Speech Model API Settings (minimaxi)
TTS_API_KEY = os.environ.get("TTS_API_KEY")
TTS_GROUP_ID = os.environ.get("TTS_GROUP_ID")
TTS_BASE_URL = os.environ.get("TTS_BASE_URL", "https://api.minimaxi.com")
TTS_MODEL_NAME = os.environ.get("TTS_MODEL_NAME", "speech-02-hd")

# =============================================================================
# Model Default Settings
# =============================================================================

MODEL_DEFAULTS = {
    "text_model": TEXT_MODEL_NAME,
    "image_model": IMAGE_MODEL_NAME,
    "tts_model": TTS_MODEL_NAME,
    "temperature": float(os.environ.get("DEFAULT_TEMPERATURE", "0.7"))
}

# Output settings
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "output")

# =============================================================================
# Helper Functions
# =============================================================================

def get_api_config(model_type: str) -> Dict[str, str]:
    """
    Get the API configuration for a specific model type.
    
    Args:
        model_type: The type of model ('text', 'image', or 'tts')
        
    Returns:
        Dictionary containing API key, base URL, and model name
    """
    configs = {
        'text': {
            'api_key': TEXT_API_KEY,
            'api_base': TEXT_BASE_URL,
            'model_name': TEXT_MODEL_NAME
        },
        'image': {
            'api_key': IMAGE_API_KEY,
            'api_base': IMAGE_BASE_URL,
            'model_name': IMAGE_MODEL_NAME
        },
        'tts': {
            'api_key': TTS_API_KEY,
            'api_base': TTS_BASE_URL,
            'model_name': TTS_MODEL_NAME,
            'group_id': TTS_GROUP_ID
        }
    }
    return configs.get(model_type, {})

def print_api_config():
    """
    Print current API configuration for debugging purposes.
    """
    print("=== API Configuration ===")
    for model_type in ['text', 'image', 'tts']:
        config = get_api_config(model_type)
        print(f"\n{model_type.upper()} Model:")
        print(f"  API Key: {'***' + config.get('api_key', 'NOT SET')[-4:] if config.get('api_key') else 'NOT SET'}")
        print(f"  Base URL: {config.get('api_base', 'NOT SET')}")
        print(f"  Model Name: {config.get('model_name', 'NOT SET')}")
        if model_type == 'tts':
            print(f"  Group ID: {'***' + config.get('group_id', 'NOT SET')[-4:] if config.get('group_id') else 'NOT SET'}")
    print("===========================") 