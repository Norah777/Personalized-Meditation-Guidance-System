#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LLM interaction logger module for recording all LLM inputs and outputs.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional


class LLMLogger:
    """Logs all LLM interactions with timestamps and metadata."""
    
    def __init__(self, log_dir: str = "logs"):
        """
        Initialize the LLM logger.
        
        Args:
            log_dir: Directory to store log files
        """
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Create a new log file for each run
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(log_dir, f"llm_interactions_{timestamp}.jsonl")
    
    def log_interaction(self, 
                       component: str,
                       prompt: str,
                       response: str,
                       metadata: Optional[Dict[str, Any]] = None):
        """
        Log a single LLM interaction.
        
        Args:
            component: Name of the component making the request
            prompt: The input prompt
            response: The LLM response
            metadata: Additional metadata about the interaction
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "component": component,
            "prompt": prompt,
            "response": response,
            "metadata": metadata or {}
        }
        
        # Append the log entry to the file
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    
    def get_log_path(self) -> str:
        """Get the path to the current log file."""
        return self.log_file 