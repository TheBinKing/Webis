import axios from "axios";

// API基础URL
const API_BASE_URL = "http://115.190.111.69:11011";

/**
 * 同步处理HTML文件
 * @param {FormData} formData 包含文件和配置的FormData对象
 * @returns {Promise} 处理结果的Promise
 */
export const processHtmlSync = async (formData) => {
  return axios.post(`${API_BASE_URL}/process-html`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

/**
 * 异步处理HTML文件（批量处理）
 * @param {FormData} formData 包含文件和配置的FormData对象
 * @param {Function} onProgress 上传进度回调函数
 * @returns {Promise} 处理结果的Promise
 */
export const processHtmlAsync = async (formData, onProgress) => {
  return axios.post(`${API_BASE_URL}/process-async`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
    onUploadProgress: onProgress,
  });
};

/**
 * 从URL获取HTML内容
 * @param {string} url 要获取内容的URL
 * @param {boolean} processContent 是否处理获取的内容
 * @returns {Promise} 包含HTML内容的Promise
 */
export const fetchHtmlFromUrl = async (url) => {
  return axios.get(`${API_BASE_URL}/fetch-url`, {
    params: {
      url: url,
    },
  });
};

/**
 * 获取任务状态
 * @param {string} taskId 任务ID
 * @returns {Promise} 任务状态的Promise
 */
export const getTaskStatus = async (taskId) => {
  return axios.get(`${API_BASE_URL}/tasks/${taskId}`);
};

/**
 * 获取任务结果
 * @param {string} taskId 任务ID
 * @returns {Promise} 任务结果的Promise
 */
export const getTaskResults = async (taskId) => {
  return axios.get(`${API_BASE_URL}/tasks/${taskId}/results`);
};

/**
 * 下载任务结果（ZIP文件）
 * @param {string} taskId 任务ID
 * @returns {Promise} 下载结果的Promise
 */
export const downloadTaskResults = async (taskId) => {
  return axios.get(`${API_BASE_URL}/tasks/${taskId}/download`, {
    responseType: "blob",
  });
};

/**
 * 直接从URL获取内容并处理
 * @param {string} url 要获取和处理的网页URL
 * @param {string} modelType 使用的模型类型，默认为"node"
 * @returns {Promise} 处理结果的Promise
 */
export const processUrl = async (url, modelType = "node") => {
  return axios.get(`${API_BASE_URL}/process-url`, {
    params: {
      url: url,
      model_type: modelType,
    },
  });
};
