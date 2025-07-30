#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Orchestrator to manage the entire pipeline flow.
"""

import os
import concurrent.futures
from typing import Dict, Any, Optional, Tuple, Generator

from pipeline.intention_recognition import IntentionRecognizer
from pipeline.prompt_creator import PromptCreator
from pipeline.image_prompt_creator import ImagePromptCreator
from pipeline.script_generator import ScriptGenerator
from pipeline.music_selector import MusicSelector
from pipeline.text_to_speech import TextToSpeech
from pipeline.video_synthesizer import VideoSynthesizer


class Orchestrator:
    """Orchestrates the entire pipeline flow."""
    
    def __init__(self):
        """Initialize all pipeline components."""
        self.intention_recognizer = IntentionRecognizer()
        self.prompt_creator = PromptCreator()
        self.image_prompt_creator = ImagePromptCreator()
        self.script_generator = ScriptGenerator()
        self.music_selector = MusicSelector()
        self.text_to_speech = TextToSpeech()
        self.video_synthesizer = VideoSynthesizer()
    
    def generate_text_only(self, user_prompt: str, emotional_state: str = "neutral") -> str:
        """
        Generate meditation text only.
        
        Args:
            user_prompt: The user's input prompt
            emotional_state: The user's emotional state
            
        Returns:
            Generated meditation text
        """
        # Step 1: Intention recognition and rewrite
        recognized_intention = self.intention_recognizer.process(
            user_prompt, emotional_state
        )
        
        # Step 2: Generate text script
        script = self.prompt_creator.create_prompt(recognized_intention)
        
        return script
    
    def generate_text_stream(self, user_prompt: str, emotional_state: str = "neutral") -> Generator[str, None, None]:
        """
        Generate meditation text with streaming output.
        
        Args:
            user_prompt: The user's input prompt
            emotional_state: The user's emotional state
            
        Yields:
            Text chunks as they are generated
        """
        # Step 1: Intention recognition and rewrite
        recognized_intention = self.intention_recognizer.process(
            user_prompt, emotional_state
        )
        
        # Step 2: Generate text script with streaming
        # For now, we'll simulate streaming by splitting the text
        # In a real implementation, you would modify the underlying model client
        # to support streaming responses
        full_text = self.prompt_creator.create_prompt(recognized_intention)
        
        # Split text into sentences for streaming effect
        sentences = full_text.split('. ')
        for i, sentence in enumerate(sentences):
            if i == len(sentences) - 1:
                yield sentence  # Last sentence, no period needed
            else:
                yield sentence + '. '
    
    def generate_image_only(self, text_content: str, output_path: str) -> str:
        """
        Generate image based on text content.
        
        Args:
            text_content: The meditation text content
            output_path: Path to save output files
            
        Returns:
            Path to the generated image file
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Create a mock intention data structure from text content
        intention_data = {
            "intention": "meditation",
            "theme": "mindfulness",
            "emotional_context": "calm",
            "key_concepts": ["peace", "tranquility", "meditation"],
            "rewritten_prompt": text_content
        }
        
        # Generate image based on the text content
        image_prompt = self.image_prompt_creator.create_prompt(intention_data)
        image_path = self.image_prompt_creator.generate_image(
            image_prompt, 
            output_path=os.path.join(output_path, "image.png")
        )
        
        return image_path
    
    def generate_video_only(self, text_content: str, image_path: Optional[str] = None, 
                          output_path: str = "output") -> str:
        """
        Generate video based on text content and optional image.
        
        Args:
            text_content: The meditation text content
            image_path: Optional path to existing image (will generate if not provided)
            output_path: Path to save output files
            
        Returns:
            Path to the generated video file
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Handle image path - convert URL path to absolute file path if needed
        if image_path is not None:
            # If image_path starts with /images/, /videos/, etc., convert to absolute path
            if image_path.startswith('/images/') or image_path.startswith('/videos/'):
                # Remove the leading slash and construct the path relative to logindemo/uploads
                relative_path = image_path[1:]  # Remove leading '/'
                # Get the project root directory (parent of my_project)
                # Current file is in my_project/pipeline/orchestrator.py
                # We need to go up two levels: pipeline -> my_project -> project_root
                current_file_dir = os.path.dirname(os.path.abspath(__file__))  # my_project/pipeline
                my_project_dir = os.path.dirname(current_file_dir)  # my_project
                project_root = os.path.dirname(my_project_dir)  # project root
                logindemo_uploads = os.path.join(project_root, "logindemo", "uploads")
                
                # Construct the full path
                full_image_path = os.path.join(logindemo_uploads, relative_path)
                
                print(f"Converting URL path {image_path} to file path: {full_image_path}")
                
                # Check if the file exists
                if os.path.exists(full_image_path):
                    image_path = full_image_path
                    print(f"Found image at: {image_path}")
                else:
                    print(f"Image file not found at: {full_image_path}")
                    # If not found, generate a new image
                    image_path = None
            elif not os.path.isabs(image_path):
                # If it's a relative path, make it absolute
                image_path = os.path.abspath(image_path)
        
        # Generate image if not provided or not found
        if image_path is None or not os.path.exists(image_path):
            print("Generating new image...")
            image_path = self.generate_image_only(text_content, output_path)
        
        print(f"Using image path: {image_path}")
        
        # Generate audio from text
        # Limit text length for audio generation
        script = text_content[:500] if len(text_content) > 500 else text_content
        # script = text_content
        
        # Save script to file
        script_path = os.path.join(output_path, "script.txt")
        with open(script_path, "w") as f:
            f.write(f"generated script:\n{script}")
        
        # Convert text to speech
        audio_path = self.text_to_speech.convert(
            script, 
            output_path=os.path.join(output_path, "narration.mp3")
        )
        
        # Select background music
        # Use absolute path to the music file
        current_file_dir = os.path.dirname(os.path.abspath(__file__))  # my_project/pipeline
        my_project_dir = os.path.dirname(current_file_dir)  # my_project
        music_path = os.path.join(my_project_dir, 'music_library', '瑜伽冥想减压音乐 - Awakening.mp3')
        
        # Create video
        video_path = self.video_synthesizer.create_video(
            image_path=image_path,
            audio_path=audio_path,
            music_path=music_path,
            output_path=os.path.join(output_path, "final_video.mp4")
        )
        
        return video_path
    
    def _text_pipeline(self, recognized_intention: Dict[str, Any], output_path: str) -> str:
        """
        Execute the text pipeline branch.
        
        Args:
            recognized_intention: The recognized user intention
            output_path: Path to save output files
            
        Returns:
            Path to the generated audio file
        """
        # Text branch: Create prompt -> Generate script -> Convert to speech
        # text_prompt = self.prompt_creator.create_prompt(recognized_intention)
        # script = self.script_generator.generate_script(text_prompt)
        script = self.prompt_creator.create_prompt(recognized_intention)
        script_path = os.path.join(output_path, "script.txt")
        with open(script_path, "w") as f:
            f.write(f"generated script:\n{script}")
        # 测试一下，限制字数
        script = script[:500]
        audio_path = self.text_to_speech.convert(
            script, 
            output_path=os.path.join(output_path, "narration.mp3")
        )
        return audio_path
    
    def _image_pipeline(self, recognized_intention: Dict[str, Any], output_path: str) -> str:
        """
        Execute the image pipeline branch.
        
        Args:
            recognized_intention: The recognized user intention
            output_path: Path to save output files
            
        Returns:
            Path to the generated image file
        """
        # Image branch: Create image prompt -> Generate image
        image_prompt = self.image_prompt_creator.create_prompt(recognized_intention)
        image_path = self.image_prompt_creator.generate_image(
            image_prompt, 
            output_path=os.path.join(output_path, "image.png")
        )
        return image_path
    
    def _music_pipeline(self, recognized_intention: Dict[str, Any], output_path: str) -> str:
        """
        Execute the music pipeline branch.
        
        Args:
            recognized_intention: The recognized user intention
            output_path: Path to save output files
            
        Returns:
            Path to the selected music file
        """
        # Music branch: Determine music type -> Select music
        '''
        music_type = self.music_selector.determine_music_type(recognized_intention)
        music_path = self.music_selector.select_music(
            music_type, 
            output_path=os.path.join(output_path, "background.mp3")
        )
        '''
        # Use absolute path to the music file
        current_file_dir = os.path.dirname(os.path.abspath(__file__))  # my_project/pipeline
        my_project_dir = os.path.dirname(current_file_dir)  # my_project
        music_path = os.path.join(my_project_dir, 'music_library', '瑜伽冥想减压音乐 - Awakening.mp3')
        return music_path
    
    def run_pipeline(self, 
                    user_prompt: str, 
                    emotional_state: str = "neutral",
                    output_path: str = "output") -> str:
        """
        Run the entire pipeline with parallel processing.
        
        Args:
            user_prompt: The user's input prompt
            emotional_state: The user's emotional state
            output_path: Path to save output files
            
        Returns:
            Path to the final output video
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Step 1: Intention recognition and rewrite
        recognized_intention = self.intention_recognizer.process(
            user_prompt, emotional_state
        )
        
        # Step 2: Execute the three branches in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # Start all pipeline branches concurrently
            text_future = executor.submit(
                self._text_pipeline, recognized_intention, output_path
            )
            image_future = executor.submit(
                self._image_pipeline, recognized_intention, output_path
            )
            music_future = executor.submit(
                self._music_pipeline, recognized_intention, output_path
            )
            
            # Collect results as they complete
            audio_path = text_future.result()
            image_path = image_future.result()
            music_path = music_future.result()
        
        # Step 3: Synthesize video from all components
        video_path = self.video_synthesizer.create_video(
            image_path=image_path,
            audio_path=audio_path,
            music_path=music_path,
            output_path=os.path.join(output_path, "final_video.mp4")
        )
        
        return video_path 