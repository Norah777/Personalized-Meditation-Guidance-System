#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main entry point for the pipeline application.
"""

import argparse
import os
from datetime import datetime
from pipeline.orchestrator import Orchestrator


def main():
    parser = argparse.ArgumentParser(description='Peace Processor Pipeline')
    parser.add_argument('--user_prompt', type=str, required=True, help='User input prompt')
    parser.add_argument('--emotional_state', type=str, default='neutral', 
                        help='User emotional state (e.g., happy, sad, anxious)')
    parser.add_argument('--output_path', type=str, default='output', 
                        help='Path to save the generated output')
    
    args = parser.parse_args()
    
    # Create a timestamped folder under the output path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamped_output_path = os.path.join(args.output_path, timestamp)
    
    # Initialize the orchestrator and run the pipeline
    orchestrator = Orchestrator()
    result = orchestrator.run_pipeline(
        user_prompt=args.user_prompt,
        emotional_state=args.emotional_state,
        output_path=timestamped_output_path
    )
    
    print(f"Pipeline execution completed. Output saved to: {result}")


if __name__ == "__main__":
    main() 