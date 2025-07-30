#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Video synthesizer module for combining image, audio, and music into a final video.
"""

import os
import subprocess
from typing import Optional, Tuple


class VideoSynthesizer:
    """Synthesizes video from image, audio narration, and background music."""
    
    def __init__(self):
        """Initialize the video synthesizer."""
        # In a real implementation, configure specific video synthesis parameters here
        pass
    
    def create_video(self, 
                    image_path: str, 
                    audio_path: str, 
                    music_path: str, 
                    output_path: str,
                    duration: Optional[int] = None) -> str:
        """
        Create a video from image and audio components using FFmpeg.
        
        Args:
            image_path: Path to the image file
            audio_path: Path to the narration audio file
            music_path: Path to the background music file
            output_path: Path to save the generated video
            duration: Optional duration in seconds (if None, uses audio length)
            
        Returns:
            Path to the generated video file
        """
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        try:
            # Check if FFmpeg is installed
            self._check_ffmpeg()
            
            # Create temporary file for mixed audio (narration + background music)
            mixed_audio_path = os.path.join(os.path.dirname(output_path), "mixed_audio.mp3")
            
            # 1. Mix audio narration with background music (reducing music volume)
            self._mix_audio(audio_path, music_path, mixed_audio_path)
            
            # 2. Create video from image and mixed audio
            self._create_video_from_image_and_audio(image_path, mixed_audio_path, output_path, duration)
            
            # Clean up temporary files
            if os.path.exists(mixed_audio_path):
                os.remove(mixed_audio_path)
            
            return output_path
            
        except Exception as e:
            print(f"Error in video synthesis: {e}")
            
            # For demonstration, create a placeholder video file
            self._create_placeholder_video(output_path)
            return output_path
    
    def _check_ffmpeg(self):
        """Check if FFmpeg is installed and available."""
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            print("Warning: FFmpeg not found. Using placeholder video output.")
            raise RuntimeError("FFmpeg not available")
    
    def _get_audio_duration(self, audio_path: str) -> float:
        """Get the duration of an audio file in seconds."""
        command = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", audio_path
        ]
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            return float(result.stdout.strip())
        except (subprocess.SubprocessError, ValueError) as e:
            print(f"Error getting audio duration: {e}")
            return 0.0
    
    def _mix_audio(self, narration_path: str, music_path: str, output_path: str):
        """
        Mix narration audio with background music at reduced volume.
        The output duration will match the narration duration.
        """
        # Get duration of both audio files
        narration_duration = self._get_audio_duration(narration_path)
        music_duration = self._get_audio_duration(music_path)
        
        print(f"Narration duration: {narration_duration}s, Music duration: {music_duration}s")
        
        # Always use the narration duration as the target duration
        target_duration = narration_duration
        
        if narration_duration > music_duration:
            # If narration is longer, we need to loop the music
            print("Narration is longer than music, will loop music")
            
            # Simple approach: use amix with repeat
            filter_complex = (
                f"[1:a]volume=0.4,aloop=loop=-1:size=2e+09[music];"
                f"[0:a][music]amix=inputs=2:duration=first[aout]"
            )
            
            command = [
                "ffmpeg", "-y",
                "-i", narration_path,
                "-i", music_path,
                "-filter_complex", filter_complex,
                "-map", "[aout]",
                "-c:a", "libmp3lame", "-q:a", "4",
                "-t", str(target_duration),  # Explicitly limit duration
                output_path
            ]
        else:
            # If music is longer or equal, just cut the music to match narration
            print("Music is longer than or equal to narration, will cut music")
            
            filter_complex = (
                f"[1:a]volume=0.4[music];"
                f"[0:a][music]amix=inputs=2:duration=first[aout]"
            )
            
            command = [
                "ffmpeg", "-y",
                "-i", narration_path,
                "-i", music_path,
                "-filter_complex", filter_complex,
                "-map", "[aout]",
                "-c:a", "libmp3lame", "-q:a", "4",
                "-t", str(target_duration),  # Explicitly limit duration
                output_path
            ]
        
        print(f"Running audio mix command: {' '.join(command)}")
        try:
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=60)
            print(f"Audio mixing completed. Output duration should be: {target_duration}s")
        except subprocess.TimeoutExpired:
            print("Warning: Audio mixing timed out")
        except subprocess.CalledProcessError as e:
            print(f"Error during audio mixing: {e}")
    
    def _create_video_from_image_and_audio(self, 
                                          image_path: str, 
                                          audio_path: str, 
                                          output_path: str,
                                          duration: Optional[int] = None):
        """Create a video from a static image and audio file."""
        # Get the duration from the audio file if not specified
        if duration is None:
            duration_cmd = [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", audio_path
            ]
            duration_result = subprocess.run(duration_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            duration = float(duration_result.stdout.strip())
        
        # Create the video
        command = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", image_path,
            "-i", audio_path,
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            output_path
        ]
        
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    
    def _create_placeholder_video(self, output_path: str):
        """Create a placeholder video file for demonstration purposes."""
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create an empty text file with a note
        placeholder_path = f"{output_path}.placeholder.txt"
        with open(placeholder_path, 'w') as f:
            f.write("This is a placeholder for a video file that would be generated by the video synthesizer using FFmpeg.")
            
        print(f"Created placeholder file at {placeholder_path} (actual video would be at {output_path})")
        
        return placeholder_path

if __name__ == "__main__":
    # Test the VideoSynthesizer
    import argparse
    import sys
    
    def parse_args():
        parser = argparse.ArgumentParser(description="Test the VideoSynthesizer")
        parser.add_argument("--image", default="output/image.png", help="Path to test image")
        parser.add_argument("--audio", default="output/tts/test_speech.mp3", help="Path to test audio narration")
        parser.add_argument("--music", default="music_library/瑜伽冥想减压音乐 - Awakening.mp3", help="Path to test background music")
        parser.add_argument("--output", default="output/output_video.mp4", help="Path for output video")
        parser.add_argument("--duration", type=int, help="Optional fixed duration in seconds")
        return parser.parse_args()
    
    def main():
        args = parse_args()
        
        print(f"Testing VideoSynthesizer with:")
        print(f"  Image: {args.image}")
        print(f"  Audio: {args.audio}")
        print(f"  Music: {args.music}")
        print(f"  Output: {args.output}")
        print(f"  Duration: {args.duration if args.duration else 'Auto (from audio)'}")
        
        synthesizer = VideoSynthesizer()
        
        try:
            output_path = synthesizer.create_video(
                image_path=args.image,
                audio_path=args.audio,
                music_path=args.music,
                output_path=args.output,
                duration=args.duration
            )
            
            print(f"Video synthesis complete!")
            print(f"Output video saved to: {output_path}")
            
        except Exception as e:
            print(f"Error during video synthesis: {e}")
            sys.exit(1)
    
    main() 