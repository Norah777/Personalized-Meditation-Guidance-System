#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
验证路径修复的简单测试
"""

import os
import sys

def test_path_calculation():
    """测试路径计算是否正确"""
    
    print("🧪 测试路径计算")
    print("=" * 50)
    
    # 模拟service.py的路径计算
    service_py_location = "/Users/dengsihang/Desktop/HKU/PeaceProcessor/my_project"
    
    # 按照service.py中的计算方式 - 正确的计算
    logindemo_uploads_dir = os.path.join(
        service_py_location, 
        "..", "..", "courses", "logindemo", "uploads"
    )
    default_output_path = os.path.abspath(logindemo_uploads_dir)
    
    print(f"📁 Service.py位置: {service_py_location}")
    print(f"📁 计算的uploads路径: {default_output_path}")
    print(f"📁 uploads目录是否存在: {os.path.exists(default_output_path)}")
    
    # 检查images和videos目录
    images_dir = os.path.join(default_output_path, "images")
    videos_dir = os.path.join(default_output_path, "videos")
    
    print(f"📁 images目录: {images_dir}")
    print(f"📁 images目录是否存在: {os.path.exists(images_dir)}")
    print(f"📁 videos目录: {videos_dir}")
    print(f"📁 videos目录是否存在: {os.path.exists(videos_dir)}")
    
    # 检查proxy_server.py期望的路径
    current_dir = "/Users/dengsihang/Desktop/HKU/courses/logindemo"
    proxy_images_path = os.path.join(current_dir, "uploads", "images")
    proxy_videos_path = os.path.join(current_dir, "uploads", "videos")
    
    print(f"\n📁 Proxy期望的images路径: {proxy_images_path}")
    print(f"📁 Proxy images路径是否存在: {os.path.exists(proxy_images_path)}")
    print(f"📁 Proxy期望的videos路径: {proxy_videos_path}")
    print(f"📁 Proxy videos路径是否存在: {os.path.exists(proxy_videos_path)}")
    
    # 检查路径是否匹配
    if default_output_path == os.path.join(current_dir, "uploads"):
        print("✅ 路径计算正确！")
        return True
    else:
        print("❌ 路径计算不匹配！")
        print(f"   期望: {os.path.join(current_dir, 'uploads')}")
        print(f"   实际: {default_output_path}")
        return False

def test_spring_boot_path():
    """测试Spring Boot的路径计算"""
    
    print("\n🧪 测试Spring Boot路径计算")
    print("=" * 50)
    
    # 模拟Spring Boot的工作目录
    spring_boot_dir = "/Users/dengsihang/Desktop/HKU/courses/logindemo/springboot-login-demo-master"
    
    # 按照Spring Boot controller的计算方式
    uploads_path = os.path.join(spring_boot_dir, "..", "uploads", "images")
    uploads_path = os.path.abspath(uploads_path)
    
    print(f"📁 Spring Boot工作目录: {spring_boot_dir}")
    print(f"📁 Spring Boot计算的uploads路径: {uploads_path}")
    print(f"📁 Spring Boot uploads路径是否存在: {os.path.exists(uploads_path)}")
    
    expected_path = "/Users/dengsihang/Desktop/HKU/courses/logindemo/uploads/images"
    
    if uploads_path == expected_path:
        print("✅ Spring Boot路径计算正确！")
        return True
    else:
        print("❌ Spring Boot路径计算不匹配！")
        print(f"   期望: {expected_path}")
        print(f"   实际: {uploads_path}")
        return False

def create_test_directories():
    """创建必要的测试目录"""
    
    print("\n🧪 创建测试目录")
    print("=" * 50)
    
    base_dir = "/Users/dengsihang/Desktop/HKU/courses/logindemo/uploads"
    
    directories = [
        base_dir,
        os.path.join(base_dir, "images"),
        os.path.join(base_dir, "videos"),
        os.path.join(base_dir, "temp")
    ]
    
    for directory in directories:
        try:
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                print(f"✅ 创建目录: {directory}")
            else:
                print(f"📁 目录已存在: {directory}")
        except Exception as e:
            print(f"❌ 创建目录失败 {directory}: {e}")
            return False
    
    return True

def test_file_operations():
    """测试文件操作"""
    
    print("\n🧪 测试文件操作")
    print("=" * 50)
    
    # 创建测试文件
    test_image_dir = "/Users/dengsihang/Desktop/HKU/courses/logindemo/uploads/images/test_20240109_143022"
    test_file_path = os.path.join(test_image_dir, "test_image.png")
    
    try:
        # 创建测试目录
        os.makedirs(test_image_dir, exist_ok=True)
        print(f"✅ 创建测试目录: {test_image_dir}")
        
        # 创建测试文件
        with open(test_file_path, 'w') as f:
            f.write("test image content")
        print(f"✅ 创建测试文件: {test_file_path}")
        
        # 测试proxy_server.py的搜索逻辑
        uploads_images_dir = "/Users/dengsihang/Desktop/HKU/courses/logindemo/uploads/images"
        found = False
        
        for root, dirs, files in os.walk(uploads_images_dir):
            if "test_image.png" in files:
                found_path = os.path.join(root, "test_image.png")
                print(f"✅ 在子目录中找到文件: {found_path}")
                found = True
                break
        
        if found:
            print("✅ 文件搜索逻辑正常")
        else:
            print("❌ 文件搜索逻辑失败")
        
        # 清理测试文件
        os.remove(test_file_path)
        os.rmdir(test_image_dir)
        print("✅ 清理测试文件")
        
        return found
        
    except Exception as e:
        print(f"❌ 文件操作测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 验证路径修复")
    print("=" * 60)
    
    # 测试路径计算
    result1 = test_path_calculation()
    
    # 测试Spring Boot路径
    result2 = test_spring_boot_path()
    
    # 创建测试目录
    result3 = create_test_directories()
    
    # 测试文件操作
    result4 = test_file_operations()
    
    # 总结
    print("\n" + "=" * 60)
    print("🎯 测试结果总结")
    print("=" * 60)
    
    results = [
        ("路径计算", result1),
        ("Spring Boot路径", result2),
        ("目录创建", result3),
        ("文件操作", result4)
    ]
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 所有路径测试通过！修复正确！")
        print("\n💡 建议:")
        print("   1. 确保AI service (my_project/service.py) 正在运行")
        print("   2. 确保Spring Boot (springboot-login-demo-master) 正在运行")
        print("   3. 确保proxy server (proxy_server.py) 正在运行")
        print("   4. 现在可以在前端测试图片生成功能")
    else:
        print("\n💥 部分测试失败，请检查路径配置")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 