#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for the new step-by-step API endpoints.
"""

import requests
import json
import time
import sys

def test_api_endpoint(endpoint, data, description):
    """Test a single API endpoint"""
    print(f"\n🧪 Testing {description}")
    print(f"📍 Endpoint: {endpoint}")
    print(f"📝 Data: {json.dumps(data, indent=2)}")
    
    try:
        start_time = time.time()
        response = requests.post(endpoint, json=data, timeout=30)
        end_time = time.time()
        
        duration = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Success! Duration: {duration:.2f}s")
                print(f"📄 Response: {json.dumps(result, indent=2)}")
                return result
            else:
                print(f"❌ Failed: {result.get('message', 'Unknown error')}")
                return None
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"❌ Timeout (30s)")
        return None
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error - Is the service running?")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Run all API tests"""
    base_url = "http://localhost:8008"
    
    print("🚀 Testing Peace Processor Pipeline - Step-by-Step APIs")
    print("=" * 60)
    
    # Test data
    test_prompt = "I feel stressed and need help with relaxation"
    test_mood = "anxious"
    
    # Test 1: Generate Text
    print("\n" + "=" * 60)
    print("TEST 1: Generate Text")
    print("=" * 60)
    
    text_data = {
        "user_prompt": test_prompt,
        "emotional_state": test_mood
    }
    
    text_result = test_api_endpoint(
        f"{base_url}/generate-text",
        text_data,
        "Text Generation"
    )
    
    if not text_result:
        print("\n❌ Text generation failed. Cannot continue with other tests.")
        sys.exit(1)
    
    generated_text = text_result.get('text', '')
    print(f"\n📝 Generated text length: {len(generated_text)} characters")
    
    # Test 2: Generate Image
    print("\n" + "=" * 60)
    print("TEST 2: Generate Image")
    print("=" * 60)
    
    image_data = {
        "text_content": generated_text,
        "output_path": "test_output"
    }
    
    image_result = test_api_endpoint(
        f"{base_url}/generate-image",
        image_data,
        "Image Generation"
    )
    
    image_path = None
    if image_result:
        image_path = image_result.get('image_path')
        print(f"\n🖼️  Generated image path: {image_path}")
    
    # Test 3: Generate Video (without existing image)
    print("\n" + "=" * 60)
    print("TEST 3: Generate Video (without existing image)")
    print("=" * 60)
    
    video_data = {
        "text_content": generated_text,
        "output_path": "test_output"
    }
    
    video_result = test_api_endpoint(
        f"{base_url}/generate-video",
        video_data,
        "Video Generation (auto-generate image)"
    )
    
    if video_result:
        video_path = video_result.get('video_path')
        print(f"\n🎥 Generated video path: {video_path}")
    
    # Test 4: Generate Video (with existing image)
    if image_path:
        print("\n" + "=" * 60)
        print("TEST 4: Generate Video (with existing image)")
        print("=" * 60)
        
        video_with_image_data = {
            "text_content": generated_text,
            "image_path": image_path,
            "output_path": "test_output"
        }
        
        video_with_image_result = test_api_endpoint(
            f"{base_url}/generate-video",
            video_with_image_data,
            "Video Generation (with existing image)"
        )
        
        if video_with_image_result:
            video_with_image_path = video_with_image_result.get('video_path')
            print(f"\n🎥 Generated video path: {video_with_image_path}")
    
    # Test 5: Health Check
    print("\n" + "=" * 60)
    print("TEST 5: Health Check")
    print("=" * 60)
    
    try:
        health_response = requests.get(f"{base_url}/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ Health check passed")
            print(f"📄 Response: {json.dumps(health_data, indent=2)}")
        else:
            print(f"❌ Health check failed: {health_response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 6: Legacy Complete Pipeline
    print("\n" + "=" * 60)
    print("TEST 6: Legacy Complete Pipeline")
    print("=" * 60)
    
    legacy_data = {
        "user_prompt": test_prompt,
        "emotional_state": test_mood,
        "output_path": "test_output"
    }
    
    legacy_result = test_api_endpoint(
        f"{base_url}/process",
        legacy_data,
        "Legacy Complete Pipeline"
    )
    
    if legacy_result:
        legacy_video_path = legacy_result.get('video_path')
        print(f"\n🎥 Legacy video path: {legacy_video_path}")
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY")
    print("=" * 60)
    
    print(f"✅ Text Generation: {'PASSED' if text_result else 'FAILED'}")
    print(f"✅ Image Generation: {'PASSED' if image_result else 'FAILED'}")
    print(f"✅ Video Generation: {'PASSED' if video_result else 'FAILED'}")
    print(f"✅ Health Check: {'PASSED' if health_response.status_code == 200 else 'FAILED'}")
    print(f"✅ Legacy Pipeline: {'PASSED' if legacy_result else 'FAILED'}")
    
    print(f"\n🎉 All tests completed!")
    
    if all([text_result, image_result, video_result]):
        print("✅ All new step-by-step APIs are working correctly!")
    else:
        print("❌ Some APIs failed. Please check the service logs.")
        sys.exit(1)

if __name__ == "__main__":
    main() 