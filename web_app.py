#!/usr/bin/env python3
"""
AI知识图谱生成器 Web界面
提供用户友好的文件上传、进度显示和结果查看功能
"""

import os
import uuid
import json
import threading
import time
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import toml
import logging

# 导入知识图谱生成功能
from src.knowledge_graph.main import process_text_in_chunks
from src.knowledge_graph.visualization import visualize_knowledge_graph
from src.knowledge_graph.llm import call_llm

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 确保必要的目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)

# 全局变量存储任务状态
task_status = {}

class TaskStatus:
    def __init__(self, task_id):
        self.task_id = task_id
        self.status = "waiting"  # waiting, processing, completed, error
        self.progress = 0
        self.current_step = ""
        self.result_file = ""
        self.json_file = ""
        self.title = ""
        self.description = ""
        self.stats = {}
        self.error_message = ""
        self.created_at = datetime.now()

def load_config():
    """加载配置文件"""
    try:
        with open('config.toml', 'r', encoding='utf-8') as f:
            return toml.load(f)
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
        return None

def generate_knowledge_graph(input_file, output_file, config, debug=False):
    """
    包装函数：调用原始的知识图谱生成功能
    """
    try:
        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            input_text = f.read()
        
        # 处理文本并提取三元组
        result = process_text_in_chunks(config, input_text, debug)
        
        if result:
            # 保存JSON数据
            json_output = output_file.replace('.html', '.json')
            with open(json_output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            # 生成可视化
            stats = visualize_knowledge_graph(result, output_file, config=config)
            
            return stats
        else:
            raise Exception("知识图谱生成失败：无法提取有效的三元组")
            
    except Exception as e:
        raise Exception(f"知识图谱生成过程中出错: {str(e)}")

def generate_content_title(text_content, config):
    """
    基于文本内容生成有意义的标题
    """
    try:
        # 创建标题生成提示词
        system_prompt = """
        你是一个专业的文本分析专家。请根据给定的文本内容，生成一个简洁、准确、有意义的标题。
        标题应该：
        1. 概括文本的主要内容或主题
        2. 长度控制在10-20个字符之间
        3. 使用中文（如果原文是中文）或英文（如果原文是英文）
        4. 避免使用特殊符号和标点
        
        只返回标题，不要返回其他内容。
        """
        
        # 截取文本前500字符用于标题生成
        text_preview = text_content[:500] if len(text_content) > 500 else text_content
        
        user_prompt = f"""
        请为以下文本内容生成一个合适的标题：

        {text_preview}
        """
        
        # 调用LLM生成标题
        model = config["llm"]["model"]
        api_key = config["llm"]["api_key"]
        max_tokens = 50
        temperature = 0.3
        base_url = config["llm"]["base_url"]
        
        title = call_llm(model, user_prompt, api_key, system_prompt, max_tokens, temperature, base_url)
        
        # 清理标题
        title = title.strip().replace('"', '').replace("'", '').replace('\n', ' ')
        
        # 如果标题太长，截取前20个字符
        if len(title) > 20:
            title = title[:20] + "..."
            
        return title if title else "未命名文档"
        
    except Exception as e:
        print(f"生成标题时出错: {e}")
        # 基于时间戳生成默认标题
        return f"知识图谱_{datetime.now().strftime('%m%d_%H%M')}"

def generate_content_description(text_content, stats, config):
    """
    基于文本内容和统计信息生成描述
    """
    try:
        system_prompt = """
        你是一个专业的文本分析专家。请根据给定的文本内容和知识图谱统计信息，生成一个简洁的描述。
        描述应该：
        1. 概括文本的主要内容领域或类型
        2. 提及关键的统计数据
        3. 长度控制在50-100个字符之间
        4. 使用中文（如果原文是中文）或英文（如果原文是英文）
        
        只返回描述，不要返回其他内容。
        """
        
        text_preview = text_content[:300] if len(text_content) > 300 else text_content
        
        user_prompt = f"""
        请为以下文本内容生成一个描述：

        文本内容：
        {text_preview}

        知识图谱统计：
        - 节点数量：{stats.get('nodes', 0)}
        - 边数量：{stats.get('edges', 0)}
        - 社区数量：{stats.get('communities', 0)}
        """
        
        model = config["llm"]["model"]
        api_key = config["llm"]["api_key"]
        max_tokens = 100
        temperature = 0.3
        base_url = config["llm"]["base_url"]
        
        description = call_llm(model, user_prompt, api_key, system_prompt, max_tokens, temperature, base_url)
        
        # 清理描述
        description = description.strip().replace('\n', ' ')
        
        if len(description) > 100:
            description = description[:100] + "..."
            
        return description if description else f"包含{stats.get('nodes', 0)}个概念和{stats.get('edges', 0)}个关系的知识图谱"
        
    except Exception as e:
        print(f"生成描述时出错: {e}")
        return f"包含{stats.get('nodes', 0)}个概念和{stats.get('edges', 0)}个关系的知识图谱"

def process_knowledge_graph(task_id, file_path, config):
    """
    后台处理知识图谱生成的任务
    """
    task = task_status[task_id]
    
    try:
        # 更新状态：开始处理
        task.status = "processing"
        task.progress = 10
        task.current_step = "读取文件内容..."
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        # 生成输出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"knowledge_graph_{timestamp}_{task_id[:8]}"
        output_file = os.path.join(app.config['RESULTS_FOLDER'], f"{base_name}.html")
        
        # 更新状态：生成标题
        task.progress = 20
        task.current_step = "生成内容标题..."
        task.title = generate_content_title(text_content, config)
        
        # 更新状态：处理文本
        task.progress = 40
        task.current_step = "提取知识三元组..."
        
        # 生成知识图谱
        stats = generate_knowledge_graph(file_path, output_file, config)
        
        # 更新状态：生成描述
        task.progress = 80
        task.current_step = "生成内容描述..."
        task.description = generate_content_description(text_content, stats, config)
        
        # 完成任务
        task.status = "completed"
        task.progress = 100
        task.current_step = "处理完成"
        task.result_file = f"{base_name}.html"
        task.json_file = f"{base_name}.json"
        task.stats = stats
        
        print(f"任务 {task_id} 处理完成")
        
    except Exception as e:
        task.status = "error"
        task.error_message = str(e)
        task.current_step = "处理失败"
        print(f"任务 {task_id} 处理失败: {e}")
    
    finally:
        # 清理上传的文件
        try:
            os.remove(file_path)
        except:
            pass

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/debug')
def debug():
    """调试页面"""
    return send_file('debug_page.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """处理文件上传"""
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return jsonify({'error': '没有文件被上传'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        # 检查文件类型
        if not file.filename.lower().endswith('.txt'):
            return jsonify({'error': '只支持 .txt 格式的文件'}), 400
        
        # 加载配置
        config = load_config()
        if not config:
            return jsonify({'error': '配置文件加载失败'}), 500
        
        # 生成任务ID
        task_id = str(uuid.uuid4())
        
        # 保存文件
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{task_id}_{filename}")
        file.save(file_path)
        
        # 创建任务状态
        task_status[task_id] = TaskStatus(task_id)
        
        # 启动后台处理线程
        thread = threading.Thread(target=process_knowledge_graph, args=(task_id, file_path, config))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': '文件上传成功，开始处理...'
        })
        
    except Exception as e:
        return jsonify({'error': f'上传失败: {str(e)}'}), 500

@app.route('/status/<task_id>')
def get_status(task_id):
    """获取任务状态"""
    if task_id not in task_status:
        return jsonify({'error': '任务不存在'}), 404
    
    task = task_status[task_id]
    
    return jsonify({
        'task_id': task.task_id,
        'status': task.status,
        'progress': task.progress,
        'current_step': task.current_step,
        'result_file': task.result_file,
        'title': task.title,
        'description': task.description,
        'stats': task.stats,
        'error_message': task.error_message
    })

@app.route('/result/<filename>')
def view_result(filename):
    """查看结果文件"""
    try:
        return send_file(os.path.join(app.config['RESULTS_FOLDER'], filename))
    except FileNotFoundError:
        return "文件不存在", 404

@app.route('/download/<filename>')
def download_result(filename):
    """下载结果文件"""
    try:
        return send_file(
            os.path.join(app.config['RESULTS_FOLDER'], filename),
            as_attachment=True,
            download_name=filename
        )
    except FileNotFoundError:
        return "文件不存在", 404

@app.route('/results')
def list_results():
    """显示历史结果页面"""
    # 获取已完成的任务
    results = []
    for task_id, task in task_status.items():
        if task.status == "completed":
            results.append({
                'task_id': task_id,
                'title': task.title,
                'description': task.description,
                'stats': task.stats,
                'created_at': task.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'result_file': task.result_file,
                'json_file': task.json_file
            })
    
    # 按创建时间倒序排列
    results.sort(key=lambda x: x['created_at'], reverse=True)
    
    return render_template('results.html', results=results)

@app.route('/api/results')
def api_get_results():
    """获取所有已完成的任务结果"""
    completed_tasks = []
    for task_id, task in task_status.items():
        if task.status == "completed":
            completed_tasks.append({
                'task_id': task_id,
                'title': task.title,
                'description': task.description,
                'stats': task.stats,
                'created_at': task.created_at.isoformat(),
                'result_file': task.result_file,
                'json_file': task.json_file
            })
    
    # 按完成时间倒序排列
    completed_tasks.sort(key=lambda x: x['created_at'], reverse=True)
    
    return jsonify(completed_tasks)

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': '文件太大，最大支持16MB'}), 413

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    print("启动AI知识图谱生成器Web界面...")
    print("访问地址: http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True) 