#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Intention recognition module that analyzes user prompts.
"""
import os
from typing import Dict, Any

from api.model_client import ModelClient
from config import settings


class IntentionRecognizer:
    """Recognizes user intention and emotional context."""
    
    def __init__(self, model_name: str = None):
        """
        Initialize the intention recognizer.
        
        Args:
            model_name: Name of the LLM model to use (defaults to settings)
        """
        self.model_client = ModelClient(model_type='text')
        self.model_name = model_name or settings.MODEL_DEFAULTS["text_model"]
    
    def process(self, user_prompt: str, emotional_state: str) -> Dict[str, Any]:
        """
        Process the user prompt to recognize intention and rewrite it.
        
        Args:
            user_prompt: The user's input prompt
            emotional_state: The user's emotional state
            
        Returns:
            Dictionary containing recognized intention and context
        """
        # Intention recognition prompt
        # Create a prompt for the LLM to analyze the user input
        analysis_prompt = f"""
Analyze the following user input and emotional state. 
Identify the primary intention, theme, and context.

User Input: {user_prompt}
Emotional State: {emotional_state}

Please provide:
1. Primary intention (e.g., relaxation, motivation, education, etc.)
2. Underlying theme (e.g., nature, success, mindfulness, etc.)
3. Emotional context (considering both the stated emotional state and the content)
4. A refined/rewritten version of the prompt that captures the essence
5. Key concepts that should be addressed

Please format the response as a JSON object with the keys: intention, theme, emotional_context, rewritten_prompt, and key_concepts.
Do not output anything else after the JSON object.
"""
        
        # Get the analysis from the LLM
        result = self.model_client.generate_text(
            prompt=analysis_prompt,
            model=self.model_name,
            temperature=0.5,  # Lower temperature for more deterministic analysis
            component="IntentionRecognizer"  # Add component name
        )
        print(f"recoginzer result:\n{result}")
        # Parse the JSON response
        # Note: In a production system, add more robust error handling
        try:
            import json
            intention_data = json.loads(result)
            return intention_data
        except json.JSONDecodeError:
            # Fallback in case the model doesn't return valid JSON
            return {
                "intention": "relaxation",  # Default fallback
                "theme": "mindfulness",
                "emotional_context": emotional_state,
                "rewritten_prompt": user_prompt,
                "key_concepts": ["peace", "calm"]
            } 