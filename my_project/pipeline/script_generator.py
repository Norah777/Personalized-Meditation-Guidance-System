#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script generator module for creating text scripts.
"""

from api.model_client import ModelClient
from config import settings


class ScriptGenerator:
    """Generates text scripts using LLM."""
    
    def __init__(self, model_name: str = None):
        """
        Initialize the script generator.
        
        Args:
            model_name: Name of the LLM model to use (defaults to settings)
        """
        self.model_client = ModelClient(model_type='text')
        self.model_name = model_name or settings.MODEL_DEFAULTS["text_model"]
    
    def generate_script(self, prompt: str) -> str:
        """
        Generate a text script based on the provided prompt.
        
        Args:
            prompt: The prompt for script generation
            
        Returns:
            Generated script text
        """
        # Add formatting instructions to the prompt
        enhanced_prompt = f"""
        {prompt}
        
        Please follow these guidelines for the script:
        - Write in a conversational, natural tone
        - Keep sentences relatively short for easier narration
        - Use appropriate pacing with natural pauses (indicated by [...])
        - Target a length of 2-3 minutes when read aloud
        - Include a gentle introduction and conclusion
        - Avoid complex jargon or technical terms
        - Use second-person perspective to connect with the listener
        
        Format the script for narration, with appropriate pauses and emphasis.
        Do not include any explanations, introductions, or additional notes.
        Just provide the script text that would be read aloud.
        """
        
        # Generate the script using the LLM
        script = self.model_client.generate_text(
            prompt=enhanced_prompt,
            model=self.model_name,
            temperature=0.7,
            max_tokens=2000,  # Allow for longer output
            component="ScriptGenerator"
        )
        
        return script.strip() 