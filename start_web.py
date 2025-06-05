#!/usr/bin/env python3
"""
简化的Web应用启动脚本，用于测试基本功能
"""

import os
import sys
from pathlib import Path

# 确保当前目录在Python路径中
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    # 尝试导入并启动Web应用
    from web_app import app
    
    print("=" * 50)
    print("🚀 AI知识图谱生成器 Web界面")
    print("=" * 50)
    print(f"📁 工作目录: {current_dir}")
    print(f"🐍 Python版本: {sys.version}")
    print("=" * 50)
    
    # 检查必要的目录
    required_dirs = ['uploads', 'results', 'templates', 'static/css', 'static/js']
    for dir_name in required_dirs:
        dir_path = current_dir / dir_name
        if dir_path.exists():
            print(f"✅ {dir_name} 目录存在")
        else:
            print(f"❌ {dir_name} 目录不存在，正在创建...")
            dir_path.mkdir(parents=True, exist_ok=True)
    
    print("=" * 50)
    print("🌐 启动Web服务器...")
    print("📍 访问地址: http://localhost:5001")
    print("⭐ 按 Ctrl+C 停止服务")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5001, debug=True)
    
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保已安装所有依赖项:")
    print("pip install Flask")
    sys.exit(1)
except Exception as e:
    print(f"❌ 启动错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 