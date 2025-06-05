#!/usr/bin/env python3
"""
测试Web应用上传功能的脚本
"""

import requests
import time
import os

def test_upload():
    """测试文件上传功能"""
    
    # 等待服务启动
    print("等待Web服务启动...")
    time.sleep(3)
    
    # 测试主页是否可访问
    try:
        response = requests.get('http://localhost:5001')
        if response.status_code == 200:
            print("✅ 主页可以正常访问")
        else:
            print(f"❌ 主页访问失败，状态码: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 无法连接到Web服务: {e}")
        return
    
    # 测试文件上传
    test_file_path = "示例文本.txt"
    if not os.path.exists(test_file_path):
        print(f"❌ 测试文件 {test_file_path} 不存在")
        return
    
    print(f"📤 测试上传文件: {test_file_path}")
    
    try:
        with open(test_file_path, 'rb') as f:
            files = {'file': (test_file_path, f, 'text/plain')}
            response = requests.post('http://localhost:5001/upload', files=files)
        
        print(f"上传响应状态码: {response.status_code}")
        print(f"上传响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            task_id = result.get('task_id')
            print(f"✅ 文件上传成功，任务ID: {task_id}")
            
            # 测试状态查询
            if task_id:
                print("📊 测试状态查询...")
                for i in range(5):
                    time.sleep(2)
                    status_response = requests.get(f'http://localhost:5001/status/{task_id}')
                    if status_response.status_code == 200:
                        status = status_response.json()
                        print(f"状态: {status.get('status')}, 进度: {status.get('progress')}%, 步骤: {status.get('current_step')}")
                        
                        if status.get('status') == 'completed':
                            print("✅ 任务完成!")
                            break
                        elif status.get('status') == 'error':
                            print(f"❌ 任务失败: {status.get('error_message')}")
                            break
                    else:
                        print(f"❌ 状态查询失败: {status_response.status_code}")
                        break
        else:
            print(f"❌ 文件上传失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 上传测试失败: {e}")

if __name__ == "__main__":
    test_upload() 