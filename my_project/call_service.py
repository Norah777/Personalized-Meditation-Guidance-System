#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Client script to call the Peace Processor Pipeline service.
"""

import argparse
import requests
import json
import sys

def call_service(user_prompt, emotional_state='neutral', output_path='output', service_url='http://localhost:8008'):
    """
    Call the pipeline service with the provided parameters.
    
    Args:
        user_prompt: User input prompt
        emotional_state: User emotional state
        output_path: Path to save the generated output
        service_url: URL of the service endpoint
        
    Returns:
        Response from the service
    """
    endpoint = f"{service_url}/process"
    
    payload = {
        "user_prompt": user_prompt,
        "emotional_state": emotional_state,
        "output_path": output_path
    }
    
    try:
        print(f"Calling service at: {endpoint}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            endpoint,
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Service call successful!")
            print(f"Video path: {result.get('video_path')}")
            print(f"Message: {result.get('message')}")
            return result
        else:
            print(f"\n❌ Service call failed with status code: {response.status_code}")
            try:
                error_info = response.json()
                print(f"Error: {error_info.get('message', 'Unknown error')}")
            except:
                print(f"Error: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Could not connect to service at {service_url}")
        print("Make sure the service is running with: python service.py")
        return None
    except Exception as e:
        print(f"\n❌ Error calling service: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Call Peace Processor Pipeline Service')
    parser.add_argument('--user_prompt', type=str, required=True, 
                        help='User input prompt')
    parser.add_argument('--emotional_state', type=str, default='neutral', 
                        help='User emotional state (e.g., happy, sad, anxious)')
    parser.add_argument('--output_path', type=str, default='output', 
                        help='Path to save the generated output')
    parser.add_argument('--service_url', type=str, default='http://localhost:8008',
                        help='URL of the pipeline service')
    
    args = parser.parse_args()
    
    # Call the service
    result = call_service(
        user_prompt=args.user_prompt,
        emotional_state=args.emotional_state,
        output_path=args.output_path,
        service_url=args.service_url
    )
    
    if result and result.get('success'):
        print(f"\n🎉 Pipeline completed successfully!")
        print(f"Final video location: {result.get('video_path')}")
        sys.exit(0)
    else:
        print(f"\n💥 Pipeline failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 