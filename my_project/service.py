#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Flask service for the Peace Processor Pipeline.
Replaces the command-line interface with a web service.
"""

import os
from datetime import datetime
from flask import Flask, request, jsonify, Response
from pipeline.orchestrator import Orchestrator

app = Flask(__name__)

# 修复路径配置 - 指向logindemo项目的uploads目录
# 当前文件位置：/Users/dengsihang/Desktop/HKU/meditation-assistant/my_project/service.py
# 目标位置：/Users/dengsihang/Desktop/HKU/meditation-assistant/logindemo/uploads/
LOGINDEMO_UPLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    "..", "logindemo", "uploads")
DEFAULT_OUTPUT_PATH = os.path.abspath(LOGINDEMO_UPLOADS_DIR)

print(f"Service.py 当前路径: {os.path.dirname(os.path.abspath(__file__))}")
print(f"目标uploads目录: {DEFAULT_OUTPUT_PATH}")
print(f"uploads目录是否存在: {os.path.exists(DEFAULT_OUTPUT_PATH)}")

# 确保uploads目录存在
if not os.path.exists(DEFAULT_OUTPUT_PATH):
    os.makedirs(DEFAULT_OUTPUT_PATH, exist_ok=True)
    print(f"创建uploads目录: {DEFAULT_OUTPUT_PATH}")

# 确保images和videos子目录存在
images_dir = os.path.join(DEFAULT_OUTPUT_PATH, "images")
videos_dir = os.path.join(DEFAULT_OUTPUT_PATH, "videos")
if not os.path.exists(images_dir):
    os.makedirs(images_dir, exist_ok=True)
    print(f"创建images目录: {images_dir}")
if not os.path.exists(videos_dir):
    os.makedirs(videos_dir, exist_ok=True)
    print(f"创建videos目录: {videos_dir}")

@app.route('/process', methods=['POST'])
def process_pipeline():
    """
    Process the pipeline request.
    
    Expected JSON payload:
    {
        "user_prompt": "string",
        "emotional_state": "string",  // optional, defaults to "neutral"
        "output_path": "string"       // optional, defaults to logindemo uploads
    }
    
    Returns:
    {
        "success": true/false,
        "video_path": "path/to/final_video.mp4",
        "message": "success/error message"
    }
    """
    try:
        # Get parameters from JSON request
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "message": "No JSON data provided"
            }), 400
        
        # Required parameter
        user_prompt = data.get('user_prompt')
        if not user_prompt:
            return jsonify({
                "success": False,
                "message": "user_prompt is required"
            }), 400
        
        # Optional parameters with defaults
        emotional_state = data.get('emotional_state', 'neutral')
        output_path = data.get('output_path', DEFAULT_OUTPUT_PATH)
        
        # Create a timestamped folder under the output path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        timestamped_output_path = os.path.join(output_path, "temp", timestamp)
        
        # Initialize the orchestrator and run the pipeline
        orchestrator = Orchestrator()
        final_video_path = orchestrator.run_pipeline(
            user_prompt=user_prompt,
            emotional_state=emotional_state,
            output_path=timestamped_output_path
        )
        return jsonify({
            "success": True,
            "video_path": final_video_path,
            "message": "Pipeline execution completed successfully"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Pipeline execution failed: {str(e)}"
        }), 500

@app.route('/generate-text', methods=['POST'])
def generate_text():
    """
    Generate meditation text only.
    
    Expected JSON payload:
    {
        "user_prompt": "string",
        "emotional_state": "string"  // optional, defaults to "neutral"
    }
    
    Returns:
    {
        "success": true/false,
        "text": "generated meditation text",
        "message": "success/error message"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "message": "No JSON data provided"
            }), 400
        
        user_prompt = data.get('user_prompt')
        if not user_prompt:
            return jsonify({
                "success": False,
                "message": "user_prompt is required"
            }), 400
        
        emotional_state = data.get('emotional_state', 'neutral')
        
        # Initialize the orchestrator and generate text only
        orchestrator = Orchestrator()
        generated_text = orchestrator.generate_text_only(
            user_prompt=user_prompt,
            emotional_state=emotional_state
        )
        
        return jsonify({
            "success": True,
            "text": generated_text,
            "message": "Text generation completed successfully"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Text generation failed: {str(e)}"
        }), 500

@app.route('/generate-image', methods=['POST'])
def generate_image():
    """
    Generate image based on text content.
    
    Expected JSON payload:
    {
        "text_content": "string",
        "session_id": "string",    // optional, for grouping related files
        "output_path": "string"    // optional, defaults to logindemo uploads
    }
    
    Returns:
    {
        "success": true/false,
        "image_path": "path/to/generated/image.png",
        "session_id": "session_id_used",
        "message": "success/error message"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "message": "No JSON data provided"
            }), 400
        
        text_content = data.get('text_content')
        if not text_content:
            return jsonify({
                "success": False,
                "message": "text_content is required"
            }), 400
        
        # 使用logindemo的uploads目录
        output_path = data.get('output_path', DEFAULT_OUTPUT_PATH)
        
        # 使用提供的session_id或生成新的时间戳
        session_id = data.get('session_id')
        if not session_id:
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create a session folder under the images directory
        timestamped_output_path = os.path.join(output_path, "images", session_id)
        
        # Initialize the orchestrator and generate image only
        orchestrator = Orchestrator()
        image_path = orchestrator.generate_image_only(
            text_content=text_content,
            output_path=timestamped_output_path
        )
        
        return jsonify({
            "success": True,
            "image_path": image_path,
            "session_id": session_id,
            "message": "Image generation completed successfully"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Image generation failed: {str(e)}"
        }), 500

@app.route('/generate-video', methods=['POST'])
def generate_video():
    """
    Generate video based on text content and image.
    
    Expected JSON payload:
    {
        "text_content": "string",
        "image_path": "string",    // optional, will generate if not provided
        "session_id": "string",    // optional, for grouping related files
        "output_path": "string"    // optional, defaults to logindemo uploads
    }
    
    Returns:
    {
        "success": true/false,
        "video_path": "path/to/final_video.mp4",
        "session_id": "session_id_used",
        "message": "success/error message"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "message": "No JSON data provided"
            }), 400
        
        text_content = data.get('text_content')
        if not text_content:
            return jsonify({
                "success": False,
                "message": "text_content is required"
            }), 400
        
        image_path = data.get('image_path')
        # 使用logindemo的uploads目录
        output_path = data.get('output_path', DEFAULT_OUTPUT_PATH)
        
        # 使用提供的session_id或生成新的时间戳
        session_id = data.get('session_id')
        if not session_id:
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create a session folder under the videos directory
        timestamped_output_path = os.path.join(output_path, "videos", session_id)
        
        # Initialize the orchestrator and generate video
        orchestrator = Orchestrator()
        video_path = orchestrator.generate_video_only(
            text_content=text_content,
            image_path=image_path,
            output_path=timestamped_output_path
        )
        
        return jsonify({
            "success": True,
            "video_path": video_path,
            "session_id": session_id,
            "message": "Video generation completed successfully"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Video generation failed: {str(e)}"
        }), 500

@app.route('/generate-text-stream', methods=['POST'])
def generate_text_stream():
    """
    Generate meditation text with streaming output.
    
    Expected JSON payload:
    {
        "user_prompt": "string",
        "emotional_state": "string"  // optional, defaults to "neutral"
    }
    
    Returns:
    Server-Sent Events stream with text chunks
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "message": "No JSON data provided"
            }), 400
        
        user_prompt = data.get('user_prompt')
        if not user_prompt:
            return jsonify({
                "success": False,
                "message": "user_prompt is required"
            }), 400
        
        emotional_state = data.get('emotional_state', 'neutral')
        
        def generate():
            try:
                # Initialize the orchestrator and generate text with streaming
                orchestrator = Orchestrator()
                for chunk in orchestrator.generate_text_stream(
                    user_prompt=user_prompt,
                    emotional_state=emotional_state
                ):
                    yield f"data: {chunk}\n\n"
                yield "data: [DONE]\n\n"
            except Exception as e:
                yield f"data: [ERROR]: {str(e)}\n\n"
        
        return Response(generate(), mimetype='text/plain')
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Stream generation failed: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Peace Processor Pipeline"
    })

if __name__ == "__main__":
    # Run the Flask service
    app.run(host='0.0.0.0', port=8008, debug=True) 