// 全局变量
let currentTaskId = null;
let statusCheckInterval = null;

// DOM元素
const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const uploadForm = document.getElementById('uploadForm');
const uploadBtn = document.getElementById('uploadBtn');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const progressCard = document.getElementById('progressCard');
const resultCard = document.getElementById('resultCard');
const progressBar = document.getElementById('progressBar');
const progressPercent = document.getElementById('progressPercent');
const currentStep = document.getElementById('currentStep');

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    console.log('页面加载完成，初始化上传功能...');
    initializeUploadArea();
    initializeForm();
});

// 初始化上传区域
function initializeUploadArea() {
    console.log('初始化上传区域...');
    
    // 点击上传区域触发文件选择
    uploadArea.addEventListener('click', (e) => {
        console.log('点击上传区域');
        // 防止按钮点击时重复触发
        if (e.target.tagName !== 'BUTTON') {
            fileInput.click();
        }
    });

    // 文件选择事件
    fileInput.addEventListener('change', handleFileSelect);

    // 拖拽事件
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // 防止页面默认的拖拽行为
    document.addEventListener('dragover', function(e) {
        e.preventDefault();
    });
    document.addEventListener('drop', function(e) {
        e.preventDefault();
    });
}

// 初始化表单
function initializeForm() {
    console.log('初始化表单...');
    uploadForm.addEventListener('submit', handleFormSubmit);
}

// 处理文件选择
function handleFileSelect(event) {
    console.log('文件选择事件触发');
    const file = event.target.files[0];
    if (file) {
        console.log('选择的文件:', file.name, file.size, file.type);
        displayFileInfo(file);
    } else {
        console.log('没有选择文件');
    }
}

// 处理拖拽悬停
function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
    uploadArea.classList.add('dragover');
    console.log('拖拽悬停');
}

// 处理拖拽离开
function handleDragLeave(event) {
    event.preventDefault();
    event.stopPropagation();
    uploadArea.classList.remove('dragover');
    console.log('拖拽离开');
}

// 处理文件拖拽
function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    uploadArea.classList.remove('dragover');
    
    console.log('文件拖拽事件触发');
    
    const files = event.dataTransfer.files;
    console.log('拖拽的文件数量:', files.length);
    
    if (files.length > 0) {
        const file = files[0];
        console.log('拖拽的文件:', file.name, file.size, file.type);
        
        if (validateFile(file)) {
            // 手动设置文件到input
            const dt = new DataTransfer();
            dt.items.add(file);
            fileInput.files = dt.files;
            displayFileInfo(file);
        }
    }
}

// 验证文件
function validateFile(file) {
    console.log('验证文件:', file.name, file.type, file.size);
    
    const maxSize = 16 * 1024 * 1024; // 16MB
    
    // 检查文件扩展名
    if (!file.name.toLowerCase().endsWith('.txt')) {
        console.log('文件格式错误');
        showAlert('请选择 .txt 格式的文件', 'warning');
        return false;
    }
    
    if (file.size > maxSize) {
        console.log('文件太大');
        showAlert('文件大小不能超过 16MB', 'warning');
        return false;
    }
    
    console.log('文件验证通过');
    return true;
}

// 显示文件信息
function displayFileInfo(file) {
    console.log('显示文件信息:', file.name);
    
    if (!validateFile(file)) {
        return;
    }
    
    fileName.textContent = file.name;
    fileSize.textContent = `(${formatFileSize(file.size)})`;
    fileInfo.classList.remove('d-none');
    uploadBtn.disabled = false;
    
    // 添加淡入动画
    fileInfo.classList.add('fade-in-up');
    
    console.log('文件信息显示完成，上传按钮已启用');
}

// 清除文件
function clearFile() {
    console.log('清除文件');
    fileInput.value = '';
    fileInfo.classList.add('d-none');
    uploadBtn.disabled = true;
    fileName.textContent = '';
    fileSize.textContent = '';
}

// 处理表单提交
async function handleFormSubmit(event) {
    event.preventDefault();
    console.log('表单提交事件触发');
    
    const file = fileInput.files[0];
    if (!file) {
        console.log('没有选择文件');
        showAlert('请选择一个文件', 'warning');
        return;
    }
    
    console.log('准备上传文件:', file.name);
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        // 禁用上传按钮
        uploadBtn.disabled = true;
        uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>上传中...';
        
        console.log('发送上传请求...');
        
        // 发送上传请求
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        console.log('上传响应状态:', response.status);
        
        const result = await response.json();
        console.log('上传响应数据:', result);
        
        if (response.ok) {
            currentTaskId = result.task_id;
            console.log('上传成功，任务ID:', currentTaskId);
            showProgressCard();
            startStatusCheck();
            showAlert('文件上传成功，开始处理...', 'success');
        } else {
            throw new Error(result.error || '上传失败');
        }
        
    } catch (error) {
        console.error('上传错误:', error);
        showAlert(error.message || '上传失败，请重试', 'danger');
        resetUploadButton();
    }
}

// 显示进度卡片
function showProgressCard() {
    console.log('显示进度卡片');
    progressCard.classList.remove('d-none');
    progressCard.classList.add('fade-in-up');
    
    // 滚动到进度卡片
    progressCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// 开始状态检查
function startStatusCheck() {
    console.log('开始状态检查');
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
    }
    
    statusCheckInterval = setInterval(checkTaskStatus, 1000);
}

// 检查任务状态
async function checkTaskStatus() {
    if (!currentTaskId) return;
    
    try {
        const response = await fetch(`/status/${currentTaskId}`);
        const status = await response.json();
        
        if (!response.ok) {
            throw new Error(status.error || '获取状态失败');
        }
        
        console.log('任务状态:', status.status, status.progress);
        updateProgress(status);
        
        if (status.status === 'completed') {
            console.log('任务完成');
            clearInterval(statusCheckInterval);
            showResult(status);
        } else if (status.status === 'error') {
            console.log('任务失败:', status.error_message);
            clearInterval(statusCheckInterval);
            showError(status.error_message);
        }
        
    } catch (error) {
        console.error('状态检查错误:', error);
        clearInterval(statusCheckInterval);
        showError('无法获取处理状态');
    }
}

// 更新进度
function updateProgress(status) {
    const progress = Math.max(0, Math.min(100, status.progress));
    
    progressBar.style.width = `${progress}%`;
    progressPercent.textContent = `${progress}%`;
    currentStep.textContent = status.current_step || '处理中...';
    
    // 更新进度条颜色
    if (progress >= 100) {
        progressBar.classList.remove('progress-bar-striped', 'progress-bar-animated');
        progressBar.style.background = 'linear-gradient(45deg, #28a745, #20c997)';
    }
}

// 显示结果
function showResult(status) {
    console.log('显示结果');
    // 隐藏进度卡片
    progressCard.classList.add('d-none');
    
    // 更新结果卡片
    document.getElementById('resultTitle').textContent = status.title || '知识图谱';
    document.getElementById('resultDescription').textContent = status.description || '处理完成';
    
    // 更新统计信息
    const stats = status.stats || {};
    document.getElementById('resultStats').innerHTML = `
        <i class="fas fa-chart-bar me-1"></i>
        节点: ${stats.nodes || 0} | 关系: ${stats.edges || 0} | 社区: ${stats.communities || 0}
    `;
    
    // 更新链接
    document.getElementById('viewResultBtn').href = `/result/${status.result_file}`;
    document.getElementById('downloadResultBtn').href = `/download/${status.result_file}`;
    
    // 显示结果卡片
    resultCard.classList.remove('d-none');
    resultCard.classList.add('fade-in-up');
    
    // 滚动到结果卡片
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // 重置表单
    resetForm();
    
    showAlert('知识图谱生成完成！', 'success');
}

// 显示错误
function showError(message) {
    console.log('显示错误:', message);
    progressCard.classList.add('d-none');
    resetForm();
    showAlert(`处理失败: ${message}`, 'danger');
}

// 重置表单
function resetForm() {
    clearFile();
    resetUploadButton();
    currentTaskId = null;
}

// 重置上传按钮
function resetUploadButton() {
    uploadBtn.disabled = true;
    uploadBtn.innerHTML = '<i class="fas fa-rocket me-2"></i>开始生成知识图谱';
}

// 显示提示信息
function showAlert(message, type = 'info') {
    console.log('显示提示:', type, message);
    
    // 创建提示框
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // 自动移除
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// 格式化文件大小
function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

// 页面卸载时清理
window.addEventListener('beforeunload', () => {
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
    }
});

// 添加全局错误处理
window.addEventListener('error', function(e) {
    console.error('JavaScript错误:', e.error);
});

// 添加一些调试信息
console.log('app.js 脚本加载完成'); 