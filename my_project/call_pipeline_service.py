#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简化的管道服务调用脚本
传入三个参数，返回final_video.mp4文件路径
"""

import argparse
import requests
import json
import sys
import time

def call_pipeline_service(user_prompt, emotional_state='neutral', output_path='output', service_url='http://localhost:8008'):
    """
    调用管道服务，传入三个参数，返回final_video.mp4文件路径
    
    Args:
        user_prompt: 用户输入提示词
        emotional_state: 情绪状态
        output_path: 输出路径
        service_url: 服务URL
        
    Returns:
        final_video.mp4的完整文件路径，格式：output_path/timestamp/final_video.mp4
    """
    endpoint = f"{service_url}/process"
    
    payload = {
        "user_prompt": user_prompt,
        "emotional_state": emotional_state,
        "output_path": output_path
    }
    
    try:
        print(f"🚀 正在调用管道服务...")
        print(f"📍 服务地址: {endpoint}")
        print(f"📝 用户提示: {user_prompt}")
        print(f"😊 情绪状态: {emotional_state}")
        print(f"📁 输出路径: {output_path}")
        print()
        
        start_time = time.time()
        
        response = requests.post(
            endpoint,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=300  # 5分钟超时
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                video_path = result.get('video_path')
                print(f"✅ 管道执行成功！")
                print(f"⏱️  用时: {duration:.2f} 秒")
                print(f"🎥 视频文件路径: {video_path}")
                return video_path
            else:
                print(f"❌ 管道执行失败: {result.get('message', '未知错误')}")
                return None
        else:
            print(f"❌ 服务调用失败，状态码: {response.status_code}")
            try:
                error_info = response.json()
                print(f"错误信息: {error_info.get('message', '未知错误')}")
            except:
                print(f"错误响应: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"❌ 服务调用超时（超过5分钟）")
        return None
    except requests.exceptions.ConnectionError:
        print(f"❌ 无法连接到服务地址: {service_url}")
        print("请确保服务已启动：python service.py (端口8008)")
        return None
    except Exception as e:
        print(f"❌ 调用服务时发生错误: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description='调用Peace Processor Pipeline服务',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python call_pipeline_service.py --user_prompt "我想要一个关于森林中冥想的指导"
  python call_pipeline_service.py --user_prompt "帮助我放松" --emotional_state "焦虑" --output_path "my_videos"
  python call_pipeline_service.py --user_prompt "晨间激励" --emotional_state "疲倦" --service_url "http://192.168.1.100:8008"
        """
    )
    
    parser.add_argument('--user_prompt', type=str, required=True, 
                        help='用户输入提示词（必需）')
    parser.add_argument('--emotional_state', type=str, default='neutral', 
                        help='用户情绪状态（默认: neutral）')
    parser.add_argument('--output_path', type=str, default='output', 
                        help='输出路径（默认: output）')
    parser.add_argument('--service_url', type=str, default='http://localhost:8008',
                        help='服务URL（默认: http://localhost:8008）')
    
    args = parser.parse_args()
    
    # 调用服务
    print("=" * 60)
    print("🌟 Peace Processor Pipeline 服务调用")
    print("=" * 60)
    
    video_path = call_pipeline_service(
        user_prompt=args.user_prompt,
        emotional_state=args.emotional_state,
        output_path=args.output_path,
        service_url=args.service_url
    )
    
    print("=" * 60)
    
    if video_path:
        print(f"🎉 任务完成！视频文件已生成:")
        print(f"📍 {video_path}")
        sys.exit(0)
    else:
        print(f"💥 任务失败！")
        sys.exit(1)

if __name__ == "__main__":
    main() 