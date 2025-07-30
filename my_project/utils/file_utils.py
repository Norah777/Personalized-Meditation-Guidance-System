#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File utilities for handling file operations.
"""

import os
import shutil
from typing import List, Optional


def ensure_directory(directory_path: str) -> str:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory_path: Path to the directory
        
    Returns:
        The directory path
    """
    os.makedirs(directory_path, exist_ok=True)
    return directory_path


def list_files(directory_path: str, extension: Optional[str] = None) -> List[str]:
    """
    List files in a directory, optionally filtering by extension.
    
    Args:
        directory_path: Path to the directory
        extension: Optional file extension to filter by (e.g., '.mp3')
        
    Returns:
        List of file paths
    """
    if not os.path.exists(directory_path):
        return []
    
    files = os.listdir(directory_path)
    
    if extension:
        files = [f for f in files if f.endswith(extension)]
    
    return [os.path.join(directory_path, f) for f in files]


def clean_directory(directory_path: str) -> None:
    """
    Remove all files in a directory.
    
    Args:
        directory_path: Path to the directory to clean
    """
    if os.path.exists(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}") 