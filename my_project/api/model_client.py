#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Model client for OpenAI API integration.
This centralizes all API calls to OpenAI models for both text (LLM) and image (VLLM).
"""

import os
import requests
import json
from typing import Dict, Any, List, Optional, Union
from config import settings
from utils.llm_logger import LLMLogger
from openai import OpenAI

class ModelClient:
    """Client for interacting with OpenAI models."""
    
    def __init__(self, 
                model_type: str = 'text',
                api_key: Optional[str] = None, 
                api_base: Optional[str] = None):
        """
        Initialize the client with OpenAI API credentials.
        
        Args:
            model_type: Type of model ('text', 'image', or 'tts')
            api_key: OpenAI API key. If None, tries to get from environment.
            api_base: OpenAI endpoint. If None, tries to get from environment.
        """
        # Get API configuration based on model type
        config = settings.get_api_config(model_type)
        
        self.api_key = api_key or config.get('api_key')
        if not self.api_key:
            raise ValueError(f"OpenAI API key is required for {model_type} model. Set it as an argument or {model_type.upper()}_API_KEY environment variable.")
        
        self.api_base = api_base or config.get('api_base')
        if not self.api_base:
            raise ValueError(f"OpenAI endpoint is required for {model_type} model. Set it as an argument or {model_type.upper()}_BASE_URL environment variable.")
        
        # Remove trailing slash if present
        if self.api_base.endswith('/'):
            self.api_base = self.api_base[:-1]
            
        # For TTS model, we also need group_id for minimaxi API
        if model_type == 'tts':
            self.group_id = config.get('group_id')
            print(self.group_id)
            if not self.group_id:
                raise ValueError("Group ID is required for TTS model. Set it as TTS_GROUP_ID environment variable.")
        
        # Initialize OpenAI client (only for text and image models)
        if model_type in ['text', 'image']:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.api_base
            )
        
        # Initialize the LLM logger
        self.logger = LLMLogger()
        
    def cut_think(self, text: str) -> str:
        """
        Cut the text after </think> tag.
        """
        if '</think>' in text:
            return text.split('</think>')[1].strip()
        else:
            return text
        
    def cut_json(self, text: str) -> str:
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0]
            return text.strip()
        else:
            return text
    
    def generate_text(self, 
                     prompt: str, 
                     model: str = None,
                     temperature: float = 0.6,
                     max_tokens: int = 8192,
                     component: str = "unknown") -> str:
        """
        Generate text using OpenAI's LLM.
        
        Args:
            prompt: The input prompt
            model: Model name to use (if None, uses default from config)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum number of tokens to generate
            component: Name of the component making the request
            
        Returns:
            Generated text response
        """
        # Use model from config if not provided
        if model is None:
            model = settings.get_api_config('text').get('model_name', 'deepseek-reasoner')
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            result = response.choices[0].message.content
            # 删去思考部分
            result = self.cut_think(result)
            # 删去json部分
            result = self.cut_json(result)
            # Log the interaction
            self.logger.log_interaction(
                component=component,
                prompt=prompt,
                response=result,
                metadata={
                    "model": model,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
            )
            
            return result
        except Exception as e:
            print(f"Error in generate_text: {e}")
            raise
    
    def generate_image(self, 
                      prompt: str,
                      model: str = None,
                      size: str = "1024x1024",
                      quality: str = "standard",
                      n: int = 1,
                      component: str = "unknown") -> str:
        """
        Generate image using OpenAI's DALL-E.
        
        Args:
            prompt: The image description
            model: Model name to use (if None, uses default from config)
            size: Image size
            quality: Image quality
            n: Number of images to generate
            component: Name of the component making the request
            
        Returns:
            URL of the generated image
        """
        # Use model from config if not provided
        if model is None:
            model = settings.get_api_config('image').get('model_name', 'dall-e-3')
        
        try:
            response = self.client.images.generate(
                model=model,
                prompt=prompt,
                n=n,
                size=size,
                quality=quality
            )
            
            image_url = response.data[0].url
            
            # Log the interaction
            self.logger.log_interaction(
                component=component,
                prompt=prompt,
                response=image_url,
                metadata={
                    "model": model,
                    "size": size,
                    "quality": quality,
                    "n": n
                }
            )
            
            return image_url
        except Exception as e:
            print(f"Error in generate_image: {e}")
            raise
    
    def text_to_speech(self,
                      text: str,
                      component: str = "unknown") -> bytes:
        """
        Convert text to speech using minimaxi's text-to-speech API.
        
        Args:
            text: The text to convert to speech
            component: Name of the component making the request
            
        Returns:
            Audio data as bytes
        """
        # Get TTS configuration
        config = settings.get_api_config('tts')
        model = config.get('model_name', 'speech-02-turbo')
        
        # Construct the API URL with group_id
        url = f"{self.api_base}/v1/t2a_v2?GroupId={self.group_id}"
        
        # Fixed payload parameters as specified by the user
        payload = json.dumps({
            "model": model,
            "text": text,
            "stream": False,
            "timber_weights": [
                {
                    "voice_id": "English_expressive_narrator",
                    "weight": 1
                }
            ],
            "voice_setting": {
                "voice_id": "",
                "speed": 0.83,
                "vol": 1,
                "pitch": 0,
                "latex_read": False
            },
            "audio_setting": {
                "sample_rate": 32000,
                "bitrate": 128000,
                "format": "mp3",
                "channel": 1
            },
            "language_boost": "auto"
        })
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            parsed_json = response.json()
            print(f"TTS API response: {parsed_json}")  # Debug info
            
            # Check if the expected structure exists
            if 'data' not in parsed_json:
                print(f"Error: 'data' field not found in response. Available keys: {list(parsed_json.keys())}")
                raise KeyError("'data' field not found in API response")
            
            if 'audio' not in parsed_json['data']:
                print(f"Error: 'audio' field not found in data. Available keys: {list(parsed_json['data'].keys())}")
                raise KeyError("'audio' field not found in data")
            
            # Extract audio data from the response
            audio_hex = parsed_json['data']['audio']
            audio_data = bytes.fromhex(audio_hex)
            
            # Log the interaction
            self.logger.log_interaction(
                component=component,
                prompt=text,
                response="[Binary audio data]",
                metadata={
                    "model": model,
                    "voice_id": "male-qn-qingse",
                    "format": "mp3"
                }
            )
            
            return audio_data
        except Exception as e:
            print(f"Error in text_to_speech: {e}")
            raise 