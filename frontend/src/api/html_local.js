import axios from "axios";

// API基础URL 
const API_BASE_URL = "http://localhost:8002";

// 创建axios实例，设置通用配置
const axiosInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

// 上传并处理 HTML 文件（同步）
export const processHtmlSync = async (formData) => {
    return axiosInstance.post('/extract/process-html', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
};

// 上传并处理 HTML 文件（异步）
export const processHtmlAsync = async (formData, onProgress) => {
    return axiosInstance.post('/extract/process-async', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: onProgress
    });
};

// 查询任务状态
export const getTaskStatus = async (taskId) => {
    return axiosInstance.get(`/tasks/${taskId}`);
};

// 下载处理结果
export const downloadTaskResults = async (taskId) => {
    return axiosInstance.get(`/tasks/${taskId}/download`, {
        responseType: 'blob'
    });
};

// 删除任务
export const deleteTask = async (taskId) => {
    return axiosInstance.delete(`/tasks/${taskId}`);
};

// 通过 URL 处理网页
export const processUrl = async (url, modelType = "node") => {
    try {
        return axiosInstance.post('/extract/process-url', null, {
            params: {
                url,
                model_type: modelType
            },
            paramsSerializer: {
                encode: (param) => param // 防止对URL进行额外编码
            }
        });
    } catch (error) {
        throw new Error('处理URL时发生错误: ' + error.message);
    }
};

// 通过 URL 抓取网页内容
export const fetchHtmlFromUrl = async (url) => {
    try {
        return axiosInstance.get('/extract/fetch-url', {
            params: { url },
            paramsSerializer: {
                encode: (param) => param // 防止对URL进行额外编码
            }
        });
    } catch (error) {
        throw new Error('抓取网页内容时发生错误: ' + error.message);
    }
};

// 检查模型服务器状态
export const checkModelServer = async () => {
    try {
        return axiosInstance.get('/utils/check-model-server');
    } catch (error) {
        throw new Error('检查模型服务器状态时发生错误: ' + error.message);
    }
};

// 安装依赖
export const installDependencies = async () => {
    try {
        return axiosInstance.get('/utils/install-dependencies');
    } catch (error) {
        throw new Error('安装依赖时发生错误: ' + error.message);
    }
};