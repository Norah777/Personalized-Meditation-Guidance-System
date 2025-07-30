#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Music selector module for determining and selecting background music.
"""

import os
import shutil
from typing import Dict, Any, List, Optional

from api.model_client import ModelClient
from config import settings


class MusicSelector:
    """Determines music type and selects music from a library."""
    
    def __init__(self, model_name: str = None):
        """
        Initialize the music selector.
        
        Args:
            model_name: Name of the LLM model to use for music type determination
        """
        self.model_client = ModelClient(model_type='text')
        self.model_name = model_name or settings.MODEL_DEFAULTS["text_model"]
        
        # Define music types and their emotional associations
        self.music_types = {
            "ambient": ["calm", "peaceful", "relaxed", "serene", "meditative"],
            "nature": ["grounded", "refreshed", "connected", "harmonious"],
            "piano": ["reflective", "emotional", "introspective", "thoughtful"],
            "positive": ["happy", "uplifted", "motivated", "inspired", "energetic"],
            "deep": ["focused", "concentrated", "deep", "intense"],
            "gentle": ["soothing", "comforting", "gentle", "soft"]
        }
        
        # Default music paths (would be replaced with actual music library)
        self.default_music = {
            "ambient": "music_library/ambient_peace.mp3",
            "nature": "music_library/nature_sounds.mp3",
            "piano": "music_library/gentle_piano.mp3",
            "positive": "music_library/uplifting.mp3",
            "deep": "music_library/deep_focus.mp3",
            "gentle": "music_library/soft_melody.mp3"
        }
        
        # Create a mock music library directory for demonstration
        self._create_mock_music_library()
    
    def _create_mock_music_library(self):
        """Create mock music library files for demonstration."""
        music_dir = "music_library"
        if not os.path.exists(music_dir):
            os.makedirs(music_dir, exist_ok=True)
            
        # Create empty placeholder files
        for music_path in self.default_music.values():
            # Ensure directory exists
            os.makedirs(os.path.dirname(music_path), exist_ok=True)
            
            # Create empty file if it doesn't exist
            if not os.path.exists(music_path):
                with open(music_path, 'w') as f:
                    f.write("This is a placeholder for a music file.")
    
    def determine_music_type(self, intention_data: Dict[str, Any]) -> str:
        """
        Determine the most appropriate music type based on intention data.
        
        Args:
            intention_data: Dictionary containing intention analysis
            
        Returns:
            Music type string
        """
        # Extract relevant data from intention analysis
        intention = intention_data.get("intention", "").lower()
        theme = intention_data.get("theme", "")
        emotional_context = intention_data.get("emotional_context", "neutral")
        
        # music selector prompt
        # Create a prompt for the LLM to determine the music type
        music_prompt = f"""
Analyze the following intention and emotional context, and select ONE of these music types that would best match:
- ambient (calm, peaceful meditative)
- nature (grounded, refreshed, connected to earth)
- piano (reflective, emotional, introspective)
- positive (happy, uplifted, motivated, energetic)
- deep (focused, concentrated, intense)
- gentle (soothing, comforting, soft)

Intention: {intention}
Theme: {theme}
Emotional Context: {emotional_context}

Return ONLY one of the music type keywords listed above, nothing else."""
        
        # Get the music type from the LLM
        result = self.model_client.generate_text(
            prompt=music_prompt,
            model=self.model_name,
            temperature=0.3,  # Lower temperature for more deterministic results
            max_tokens=50,  # Short response needed
            component="MusicSelector"
        )
        
        # Clean up the result to get just the music type
        music_type = result.strip().lower()
        
        # Validate that the music type is one of the ones we recognize
        if music_type not in self.music_types:
            # Default to ambient if the model returns something unexpected
            music_type = "ambient"
        
        return music_type
    
    def select_music(self, music_type: str, output_path: str) -> str:
        """
        Select a background music file based on the determined music type.
        In a real implementation, this would select from a library of music files.
        
        Args:
            music_type: Type of music to select
            output_path: Path to save/copy the selected music file
            
        Returns:
            Path to the selected music file
        """
        # Get the default music file for the specified type
        source_path = self.default_music.get(music_type, self.default_music["ambient"])
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Copy the music file to the output location
        shutil.copy2(source_path, output_path)
        
        return output_path 