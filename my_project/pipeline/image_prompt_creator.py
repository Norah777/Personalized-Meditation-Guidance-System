#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Image prompt creator module for generating VLLM prompts.
"""

import os
import requests
from typing import Dict, Any, Optional
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
from dashscope import ImageSynthesis

from api.model_client import ModelClient
from config import settings


class ImagePromptCreator:
    """Creates prompts for image generation and handles image generation."""
    
    def __init__(self, 
                text_model: str = None, 
                image_model: str = None):
        """
        Initialize the image prompt creator.
        
        Args:
            text_model: Name of the LLM model to use for prompt enhancement
            image_model: Name of the image model to use (not used with dashscope)
        """
        # Initialize text model client for prompt enhancement
        self.text_client = ModelClient(model_type='text')
        
        # Text model for prompt enhancement
        self.text_model = text_model or settings.MODEL_DEFAULTS["text_model"]
        
        # Get API key from environment variable
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            print("Warning: DASHSCOPE_API_KEY environment variable not found")
    
    def create_prompt(self, intention_data: Dict[str, Any]) -> str:
        """
        Create a prompt for image generation based on recognized intention.
        
        Args:
            intention_data: Dictionary containing intention analysis
            
        Returns:
            A detailed image generation prompt
        """
        # Extract data from the intention analysis
        intention = intention_data.get("intention", "").lower()
        theme = intention_data.get("theme", "mindfulness")
        emotional_context = intention_data.get("emotional_context", "neutral")
        key_concepts = intention_data.get("key_concepts", ["peace", "calm"])
        
        # Convert key concepts list to string
        key_concepts_str = ", ".join(key_concepts) if isinstance(key_concepts, list) else key_concepts
        
        # Create base prompt
        base_prompt = f"""
        Create a {intention}-focused image that captures the essence of {theme}.
        The image should convey a sense of {emotional_context} and incorporate elements of {key_concepts_str}.
        """
        
        # image prompt creator prompt
        # Use LLM to enhance the base prompt with more details
        enhancement_prompt = f"""
Create a detailed, vivid, and specific image generation prompt based on the following theme and concepts.
Make it suitable for an AI image generator (like DALL-E) by including specific visual elements,
lighting, mood, style, and composition details.

Base prompt: {base_prompt}

The image should be:
- High quality and aesthetically pleasing
- Suitable for a meditation or mindfulness video
- Emotionally resonant with the theme and concepts
- Not containing any text or human faces
- Avoiding any controversial, disturbing or explicit content

Enhance the prompt with specific details about:
- Visual elements and symbolism
- Color palette and lighting
- Artistic style
- Composition and perspective

Return ONLY the enhanced prompt text, without any explanations, introductions or additional notes."""
        
        # Get the enhanced prompt from the LLM
        # 强化prompt
        enhanced_prompt = self.text_client.generate_text(
            prompt=enhancement_prompt,
            model=self.text_model,
            temperature=0.6,  # More creative for image descriptions
            component="ImagePromptCreator_Text"
        )
        # enhanced_prompt = base_prompt
        
        return enhanced_prompt
    
    def generate_image(self, image_prompt: str, output_path: str) -> str:
        """
        Generate an image based on the prompt and save it using DashScope.
        
        Args:
            image_prompt: The detailed image generation prompt
            output_path: Path to save the generated image
            
        Returns:
            Path to the saved image
        """
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY environment variable is required")
            
        try:
            print(f"Generating image with DashScope...")
            print(f"Prompt: {image_prompt}")
            
            # Call DashScope ImageSynthesis API
            rsp = ImageSynthesis.call(
                api_key=self.api_key,
                model=ImageSynthesis.Models.wanx_v1,
                prompt=image_prompt,
                n=1,
                style='<watercolor>',
                size='1024*1024'
            )
            
            print(f'DashScope response status: {rsp.status_code}')
            
            if rsp.status_code == HTTPStatus.OK:
                # Ensure directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Download and save the image
                for result in rsp.output.results:
                    print(f"Downloading image from: {result.url}")
                    response = requests.get(result.url)
                    response.raise_for_status()
                    
                    # Save image to the specified path
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    
                    print(f"Image saved to: {output_path}")
                    return output_path
            else:
                print(f'Image generation failed, status_code: {rsp.status_code}, code: {rsp.code}, message: {rsp.message}')
                raise Exception(f"DashScope API error: {rsp.code} - {rsp.message}")
                
        except Exception as e:
            print(f"Error generating image with DashScope: {e}")
            raise


if __name__ == "__main__":
    import argparse
    import sys
    
    def parse_args():
        parser = argparse.ArgumentParser(description="Test ImagePromptCreator")
        parser.add_argument("--theme", default="mindfulness", help="Image theme")
        parser.add_argument("--intention", default="relaxation", help="User intention")
        parser.add_argument("--emotional-context", default="peaceful", help="Emotional context")
        parser.add_argument("--key-concepts", nargs="+", default=["peace", "calm", "nature"], help="Key concepts")
        parser.add_argument("--output", default="output/test_image_with_augmented_prompt.png", help="Output image path")
        parser.add_argument("--skip-prompt-generation", action="store_true", help="Skip LLM prompt generation and use simple prompt")
        return parser.parse_args()
    
    def main():
        args = parse_args()
        
        print("=== Testing ImagePromptCreator ===")
        print(f"Theme: {args.theme}")
        print(f"Intention: {args.intention}")
        print(f"Emotional Context: {args.emotional_context}")
        print(f"Key Concepts: {args.key_concepts}")
        print(f"Output Path: {args.output}")
        print()
        
        # Create test intention data
        intention_data = {
            "intention": args.intention,
            "theme": args.theme,
            "emotional_context": args.emotional_context,
            "key_concepts": args.key_concepts
        }
        
        try:
            # Initialize the ImagePromptCreator
            creator = ImagePromptCreator()
            
            if args.skip_prompt_generation:
                # Use a simple test prompt instead of generating one
                image_prompt = f"A peaceful {args.theme} scene with {', '.join(args.key_concepts)}, {args.emotional_context} mood, watercolor style, no text, no people"
                print("Using simple test prompt:")
                print(f"Prompt: {image_prompt}")
            else:
                # Step 1: Create image prompt
                print("Step 1: Creating enhanced image prompt...")
                image_prompt = creator.create_prompt(intention_data)
                print(f"Generated prompt: {image_prompt}")
            
            print()
            
            # Step 2: Generate image
            print("Step 2: Generating image with DashScope...")
            output_path = creator.generate_image(image_prompt, args.output)
            
            print(f"✅ Success! Image generated and saved to: {output_path}")
            
            # Check if file exists and get size
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"📁 File size: {file_size:,} bytes")
            
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            sys.exit(1)
    
    main() 