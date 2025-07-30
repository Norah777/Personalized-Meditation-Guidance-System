#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试图片生成修复的脚本
"""

import requests
import json
import os
import sys

def test_image_generation():
    """测试图片生成功能"""
    
    print("🧪 测试图片生成修复")
    print("=" * 50)
    
    # 测试数据
    test_data = {
        "user_prompt": "我需要放松",
        "emotional_state": "stressed"
    }
    
    service_url = "http://localhost:8008"
    
    # 第一步：生成文本
    print("\n1. 测试文本生成...")
    try:
        response = requests.post(
            f"{service_url}/generate-text",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                generated_text = result.get('text', '')
                print(f"✅ 文本生成成功，长度: {len(generated_text)}")
                print(f"📝 文本预览: {generated_text[:100]}...")
            else:
                print(f"❌ 文本生成失败: {result.get('message')}")
                return False
        else:
            print(f"❌ 服务调用失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 文本生成错误: {e}")
        return False
    
    # 第二步：生成图片
    print("\n2. 测试图片生成...")
    try:
        image_data = {
            "text_content": generated_text
        }
        
        response = requests.post(
            f"{service_url}/generate-image",
            json=image_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                image_path = result.get('image_path', '')
                print(f"✅ 图片生成成功")
                print(f"📁 图片路径: {image_path}")
                
                # 检查文件是否存在
                if os.path.exists(image_path):
                    print(f"✅ 图片文件存在，大小: {os.path.getsize(image_path)} bytes")
                    
                    # 检查是否在uploads目录中
                    if "uploads" in image_path and "images" in image_path:
                        print("✅ 图片已保存到uploads/images目录")
                        return True
                    else:
                        print("⚠️  图片未保存到uploads/images目录")
                        return False
                else:
                    print(f"❌ 图片文件不存在: {image_path}")
                    return False
            else:
                print(f"❌ 图片生成失败: {result.get('message')}")
                return False
        else:
            print(f"❌ 图片生成请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 图片生成错误: {e}")
        return False

def test_spring_boot_integration():
    """测试Spring Boot集成"""
    
    print("\n🧪 测试Spring Boot集成")
    print("=" * 50)
    
    backend_url = "http://localhost:8081"
    
    # 测试文本生成
    print("\n1. 测试Spring Boot文本生成...")
    try:
        import urllib.parse
        
        data = {
            'userId': 123,
            'mood': 'stressed',
            'content': '我需要放松'
        }
        
        response = requests.post(
            f"{backend_url}/mood-logs/generateText",
            data=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'text' in result:
                generated_text = result['text']
                print(f"✅ Spring Boot文本生成成功，长度: {len(generated_text)}")
                print(f"📝 文本预览: {generated_text[:100]}...")
            else:
                print(f"❌ Spring Boot文本生成失败: {result}")
                return False
        else:
            print(f"❌ Spring Boot文本生成请求失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Spring Boot文本生成错误: {e}")
        return False
    
    # 测试图片生成
    print("\n2. 测试Spring Boot图片生成...")
    try:
        data = {
            'userId': 123,
            'textContent': generated_text
        }
        
        response = requests.post(
            f"{backend_url}/mood-logs/generateImage",
            data=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'imageUrl' in result:
                image_url = result['imageUrl']
                print(f"✅ Spring Boot图片生成成功")
                print(f"🔗 图片URL: {image_url}")
                
                # 测试图片访问
                print("\n3. 测试图片访问...")
                try:
                    proxy_url = "http://localhost:8080"
                    image_response = requests.get(f"{proxy_url}{image_url}", timeout=10)
                    
                    if image_response.status_code == 200:
                        print(f"✅ 图片访问成功，大小: {len(image_response.content)} bytes")
                        print(f"📄 Content-Type: {image_response.headers.get('Content-Type')}")
                        return True
                    else:
                        print(f"❌ 图片访问失败: {image_response.status_code}")
                        return False
                        
                except Exception as e:
                    print(f"❌ 图片访问错误: {e}")
                    return False
                    
            else:
                print(f"❌ Spring Boot图片生成失败: {result}")
                return False
        else:
            print(f"❌ Spring Boot图片生成请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Spring Boot图片生成错误: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 测试图片生成修复")
    print("=" * 60)
    
    # 检查服务状态
    print("\n📋 检查服务状态...")
    
    services = [
        ("AI Service", "http://localhost:8008/health"),
        ("Spring Boot", "http://localhost:8081/actuator/health"),
        ("Proxy Server", "http://localhost:8080")
    ]
    
    for name, url in services:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name} 运行正常")
            else:
                print(f"⚠️  {name} 状态异常: {response.status_code}")
        except Exception as e:
            print(f"❌ {name} 不可访问: {e}")
    
    # 测试AI服务
    print("\n" + "=" * 60)
    result1 = test_image_generation()
    
    # 测试Spring Boot集成
    print("\n" + "=" * 60)
    result2 = test_spring_boot_integration()
    
    # 总结
    print("\n" + "=" * 60)
    print("🎯 测试结果总结")
    print("=" * 60)
    
    if result1:
        print("✅ AI服务图片生成: 通过")
    else:
        print("❌ AI服务图片生成: 失败")
    
    if result2:
        print("✅ Spring Boot集成: 通过")
    else:
        print("❌ Spring Boot集成: 失败")
    
    if result1 and result2:
        print("\n🎉 所有测试通过！图片生成修复成功！")
        return True
    else:
        print("\n💥 部分测试失败，请检查日志")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 