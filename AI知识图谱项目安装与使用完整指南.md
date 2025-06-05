# AI知识图谱项目安装与使用完整指南

## 📋 项目概述

AI知识图谱生成器是一个基于Python的工具，能够从文本文档中提取实体和关系，并生成交互式的知识图谱可视化。项目版本：0.6.1

## 🚨 问题背景

在安装过程中遇到了两个关键问题：
1. **SSL证书验证失败** - macOS系统常见的网络连接问题
2. **Python版本不兼容** - 项目要求Python ≥3.12，而系统使用的是Python 3.11.9

## 🔧 完整解决方案

### 第一步：问题诊断

#### 1.1 查看错误信息
```bash
pip install -r requirements.txt
```
错误症状：
- SSL证书验证失败：`[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed`
- Python版本不兼容：`Package 'ai-knowledge-graph' requires a different Python: 3.11.9 not in '>=3.12'`

#### 1.2 检查项目结构
```bash
ls -la
```
项目包含的关键文件：
- `requirements.txt` - 依赖项列表
- `pyproject.toml` - 项目配置和Python版本要求
- `generate-graph.py` - 主执行脚本
- `src/` - 源代码目录

### 第二步：安装正确的Python版本

#### 2.1 检查当前Python版本
```bash
python3 --version
# 输出：Python 3.11.9 (不满足要求)
```

#### 2.2 使用Homebrew安装Python 3.12
```bash
brew install python@3.12
```

安装完成后，Python 3.12将安装在：
- 可执行文件：`/opt/homebrew/bin/python3.12`
- 库文件：`/opt/homebrew/Cellar/python@3.12/3.12.10_1/`

#### 2.3 验证安装
```bash
python3.12 --version
# 输出：Python 3.12.10
```

### 第三步：创建虚拟环境

#### 3.1 使用Python 3.12创建虚拟环境
```bash
python3.12 -m venv venv
```

这将在项目根目录创建一个名为`venv`的虚拟环境文件夹。

#### 3.2 激活虚拟环境
```bash
source venv/bin/activate
```

激活成功的标志：命令提示符前出现`(venv)`前缀。

### 第四步：安装项目依赖

#### 4.1 升级pip（可选）
```bash
pip install --upgrade pip
```

#### 4.2 安装项目依赖
```bash
pip install -r requirements.txt
```

安装的主要包包括：
- `networkx>=3.4.2` - 图形分析库
- `pyvis>=0.3.2` - 图形可视化库
- `requests>=2.32.3` - HTTP请求库
- `pandas>=2.2.3` - 数据处理库
- `numpy>=2.2.4` - 数值计算库
- 以及其他依赖项

### 第五步：验证安装

#### 5.1 检查Python版本
```bash
python --version
# 输出：Python 3.12.10
```

#### 5.2 检查已安装的包
```bash
pip list
```

#### 5.3 测试项目脚本
```bash
# 方法1：直接运行Python脚本
python generate-graph.py --help

# 方法2：使用安装的命令行工具
generate-graph --help
```

两种方法都应该显示帮助信息，包括所有可用的命令行选项。

### 第六步：运行测试

#### 6.1 生成示例知识图谱
```bash
generate-graph --test
```

成功执行的输出示例：
```
Generating sample data visualization...
Generating sample visualization with 21 triples
Edge style: Straight (no smoothing)
Processing 21 triples for visualization
Found 19 unique nodes
Found 0 inferred relationships
Detected 3 communities using Louvain method
Nodes in NetworkX graph: 19
Edges in NetworkX graph: 21
Knowledge graph visualization saved to knowledge_graph.html
```

#### 6.2 验证生成的文件
```bash
ls -la knowledge_graph.html
# 应该显示一个约747KB的HTML文件
```

#### 6.3 在浏览器中打开可视化
```bash
open knowledge_graph.html
```

## 🎯 使用指南

### 基本命令

1. **生成测试图谱**
   ```bash
   generate-graph --test
   ```

2. **从文本文件生成图谱**
   ```bash
   generate-graph --input your_text_file.txt
   ```

3. **指定输出文件**
   ```bash
   generate-graph --input input.txt --output my_graph.html
   ```

4. **启用调试模式**
   ```bash
   generate-graph --input input.txt --debug
   ```

5. **禁用实体标准化**
   ```bash
   generate-graph --input input.txt --no-standardize
   ```

6. **禁用关系推理**
   ```bash
   generate-graph --input input.txt --no-inference
   ```

### 配置选项

项目支持通过配置文件进行自定义：
```bash
generate-graph --config config.toml --input input.txt
```

## 🔍 故障排除

### 常见问题与解决方案

#### 问题1：命令未找到 (command not found)
**症状：** `zsh: command not found: python` 或 `command not found: generate-graph`

**解决方案：**
```bash
# 确保虚拟环境已激活
source venv/bin/activate
# 命令提示符应该显示 (venv)
```

#### 问题2：SSL证书错误
**症状：** `[SSL: CERTIFICATE_VERIFY_FAILED]`

**解决方案：**
```bash
# 跳过SSL验证安装（临时解决方案）
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

#### 问题3：Python版本不兼容
**症状：** `requires a different Python: 3.11.9 not in '>=3.12'`

**解决方案：**
1. 安装Python 3.12或更高版本
2. 使用正确版本创建虚拟环境
3. 在虚拟环境中安装依赖

#### 问题4：权限错误
**症状：** Permission denied错误

**解决方案：**
```bash
# 确保在虚拟环境中操作，避免使用sudo
source venv/bin/activate
pip install -r requirements.txt
```

#### 问题5：AI模型未找到
**症状：** `model "gemma3" not found, try pulling it first`

**原因：** 配置文件中的模型名称与实际安装的模型不匹配

**解决方案：**
1. **检查已安装的模型：**
   ```bash
   ollama list
   ```

2. **修改配置文件 `config.toml`：**
   ```toml
   [llm]
   model = "gemma3:27b"  # 修改为实际安装的模型名称
   # 或使用其他本地模型
   # model = "qwen3:32b"
   # model = "llama3-2-90b-instruct"
   ```

3. **确保Ollama服务运行：**
   ```bash
   # 检查服务状态
   curl -s http://localhost:11434/api/tags
   ```

#### 问题6：中文文本处理和输出中文化

**问题背景：** 
当处理中文文本时，默认的英文提示词会导致输出的实体和关系仍然是英文，例如"State Council"、"Government Departments"等，而我们需要中文化的输出如"国务院"、"政府部门"等。

**解决方案：**

我们已经实现了完整的中文化处理系统，包括：

1. **智能语言检测：**
   - 系统会自动检测输入文本是否主要为中文（中文字符占比>30%）
   - 根据检测结果选择相应的处理策略

2. **中文化提示词：**
   - 修改了 `src/knowledge_graph/prompts.py` 中的所有提示词
   - 添加了本地化指令，要求LLM在处理中文文本时输出中文实体和关系
   - 提供了中文和英文两套示例格式

3. **中文实体标准化：**
   - 在 `src/knowledge_graph/entity_standardization.py` 中添加了中文特殊处理
   - 中文停用词过滤：去除"的"、"是"、"了"、"在"等常见字符
   - 中文实体相似性检测：基于字符级别的包含和重叠关系
   - 中文关系推理：使用"关联"、"相关"等中文谓词

4. **测试中文化效果：**
   ```bash
   # 激活虚拟环境
   source venv/bin/activate
   
   # 处理中文文本生成知识图谱
   generate-graph --input data/gov-data.txt --output chinese-graph.html
   ```

**成功效果示例：**
- **中文实体：** 国务院、政务数据共享、李强、政府部门、数据共享主管部门
- **中文关系：** 发布、通过、生效、总理、依据、适用、负责、建立、包括
- **推理关系：** 关联、相关、涉及、属于、需要、影响、限制

**最终输出统计：**
- 节点：44个（全中文实体）
- 边：269条（原始102条 + 推理167条）
- 社区：4个
- 语言：完全中文化的知识图谱

## 📁 项目文件结构

```
ai-knowledge-graph/
├── venv/                    # 虚拟环境（新创建）
├── src/                     # 源代码目录
├── data/                    # 数据目录
├── docs/                    # 文档目录
├── requirements.txt         # 依赖项列表
├── pyproject.toml          # 项目配置
├── generate-graph.py       # 主执行脚本
├── config.toml             # 配置文件
├── knowledge_graph.html    # 生成的可视化文件
├── gov-knowledge-graph.html # 政府数据知识图谱示例
├── gov-knowledge-graph.json # 原始知识图谱数据
├── README.md               # 项目说明
└── LICENSE                 # 许可证
```

## ⚠️ 重要注意事项

### 每次使用前的必要步骤

1. **进入项目目录：**
   ```bash
   cd /Users/huangying/github/ai-knowledge-graph
   ```

2. **激活虚拟环境：**
   ```bash
   source venv/bin/activate
   ```

3. **确认激活成功：**
   - 命令提示符显示 `(venv)`
   - `python --version` 显示 Python 3.12.10

4. **确保Ollama服务运行：**
   ```bash
   # 检查服务状态
   curl -s http://localhost:11434/api/tags > /dev/null && echo "Ollama运行正常" || echo "Ollama未运行"
   ```

### 退出虚拟环境

当不再使用项目时：
```bash
deactivate
```

### 系统要求

- **操作系统：** macOS (测试环境: darwin 24.5.0)
- **Python版本：** ≥3.12
- **Shell：** zsh (默认)
- **包管理器：** Homebrew (推荐)
- **AI模型服务：** Ollama (本地AI模型运行)

## 🎉 成功标志

安装成功的标志：
1. ✅ `generate-graph --help` 显示帮助信息
2. ✅ `generate-graph --test` 成功生成示例图谱
3. ✅ 生成的 `knowledge_graph.html` 文件可以在浏览器中正常显示
4. ✅ 图谱显示19个节点、21条边、3个社区

实际使用成功的标志：
1. ✅ `generate-graph --input data/gov-data.txt` 成功处理真实数据
2. ✅ 生成包含36个节点、270条边、4个社区的复杂知识图谱
3. ✅ AI模型正确提取和推理实体关系
4. ✅ 可视化效果良好，支持交互操作

## 📞 技术支持

如遇到问题，请检查：
1. 虚拟环境是否正确激活
2. Python版本是否为3.12+
3. 所有依赖包是否正确安装
4. Ollama服务是否正在运行
5. 配置文件中的模型名称是否正确
6. 网络连接是否正常

---

**文档创建时间：** 2024年6月4日  
**最后更新：** 2024年6月4日  
**项目版本：** ai-knowledge-graph v0.6.1  
**Python版本：** 3.12.10  
**AI模型：** gemma3:27b (Ollama)  
**测试环境：** macOS Sequoia 15.5.0