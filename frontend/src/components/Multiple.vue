<template>
  <div class="multiple-container">
    <div class="title-section">
      <h1>批量清洗</h1>
      <p>上传包含HTML文件的文件夹，进行批量页面清洗处理</p>
    </div>

    <div class="upload-section">
      <div
        class="upload-card"
        @click="triggerFileInput"
        @dragover.prevent="onDragOver"
        @drop.prevent="onDrop"
      >
        <div class="upload-icon">
          <el-icon :size="32"><Folder /></el-icon>
        </div>
        <div class="upload-text">
          <p>点击选择文件夹或拖拽至此处</p>
          <p class="upload-hint">支持包含多个HTML文件的文件夹</p>
        </div>
        <input
          ref="fileInput"
          type="file"
          webkitdirectory
          directory
          multiple
          style="display: none"
          @change="onFileChange"
        />
      </div>
    </div>

    <div v-if="selectedFiles.length > 0" class="file-list">
      <div class="list-header">
        <h3>已选择 {{ selectedFiles.length }} 个文件</h3>
        <div class="actions">
          <el-button size="small" @click="clearFiles">清空</el-button>
          <el-button
            type="primary"
            size="small"
            @click="startProcessing"
            :loading="processing"
            >开始处理</el-button
          >
        </div>
      </div>
      <div class="files">
        <div
          v-for="(file, index) in displayedFiles"
          :key="index"
          class="file-item"
        >
          <el-icon><Document /></el-icon>
          <span class="file-name">{{ file.name }}</span>
          <span class="file-size">{{ formatFileSize(file.size) }}</span>
        </div>
        <div v-if="selectedFiles.length > 5" class="more-files">
          还有 {{ selectedFiles.length - 5 }} 个文件...
        </div>
      </div>
    </div>

    <div v-if="processing || taskStatus" class="progress-section">
      <div class="progress-card">
        <div class="progress-header">
          <h3>处理进度</h3>
          <el-tag v-if="taskStatus" :type="getStatusType">{{
            getStatusText
          }}</el-tag>
        </div>
        <div v-if="processing && !taskId" class="uploading">
          <el-progress type="circle" :percentage="uploadProgress" />
          <p>正在上传文件...</p>
        </div>
        <div
          v-else-if="
            taskId && taskStatus !== 'completed' && taskStatus !== 'failed'
          "
          class="processing"
        >
          <el-progress
            type="circle"
            :percentage="50"
            status="success"
            indeterminate
          />
          <p>正在处理文件，请稍候...</p>
        </div>
        <div v-else-if="taskStatus === 'completed'" class="completed">
          <div class="success-icon">
            <el-icon :size="48"><SuccessFilled /></el-icon>
          </div>
          <p>处理完成！</p>
          <div class="action-buttons">
            <el-button type="primary" @click="downloadResults"
              >下载结果</el-button
            >
            <el-button @click="viewResults">查看结果</el-button>
          </div>
        </div>
        <div v-else-if="taskStatus === 'failed'" class="failed">
          <div class="error-icon">
            <el-icon :size="48"><CircleCloseFilled /></el-icon>
          </div>
          <p>处理失败: {{ errorMessage }}</p>
          <el-button @click="resetProcess">重新尝试</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import {
  Document,
  Folder,
  SuccessFilled,
  CircleCloseFilled,
} from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
// 导入封装的API
import {
  processHtmlAsync,
  getTaskStatus,
  downloadTaskResults,
} from "@/api/html_local";

const router = useRouter();
const fileInput = ref(null);
const selectedFiles = ref([]);
const processing = ref(false);
const uploadProgress = ref(0);
const taskId = ref(null);
const taskStatus = ref(null);
const errorMessage = ref("");
const checkStatusInterval = ref(null);

// 只显示前5个文件
const displayedFiles = computed(() => {
  return selectedFiles.value.slice(0, 5);
});

const getStatusType = computed(() => {
  switch (taskStatus.value) {
    case "processing":
      return "info";
    case "completed":
      return "success";
    case "failed":
      return "danger";
    default:
      return "info";
  }
});

const getStatusText = computed(() => {
  switch (taskStatus.value) {
    case "processing":
      return "处理中";
    case "completed":
      return "已完成";
    case "failed":
      return "失败";
    default:
      return "等待中";
  }
});

// 触发文件选择器
const triggerFileInput = () => {
  fileInput.value.click();
};

// 文件改变事件
const onFileChange = (event) => {
  const files = Array.from(event.target.files);
  // 只选择HTML文件
  const htmlFiles = files.filter(
    (file) => file.name.endsWith(".html") || file.type === "text/html"
  );

  if (htmlFiles.length === 0) {
    ElMessage.warning("未找到HTML文件，请确保文件夹中包含HTML文件");
    return;
  }

  selectedFiles.value = htmlFiles;
  ElMessage.success(`已选择 ${htmlFiles.length} 个HTML文件`);
};

// 拖拽事件
const onDragOver = (event) => {
  event.preventDefault();
};

const onDrop = (event) => {
  event.preventDefault();

  // 处理拖放的文件夹中的所有文件
  const items = event.dataTransfer.items;
  const files = [];

  // 遍历所有拖放的项目
  for (let i = 0; i < items.length; i++) {
    const item = items[i].webkitGetAsEntry();
    if (item) {
      traverseFileTree(item, files);
    }
  }
};

// 递归遍历文件树
const traverseFileTree = (item, files) => {
  if (item.isFile) {
    // 如果是文件，检查是否为HTML文件
    item.file((file) => {
      if (file.name.endsWith(".html") || file.type === "text/html") {
        files.push(file);
        selectedFiles.value = [...selectedFiles.value, file];
      }
    });
  } else if (item.isDirectory) {
    // 如果是目录，获取目录下的所有条目
    const dirReader = item.createReader();
    dirReader.readEntries((entries) => {
      for (let i = 0; i < entries.length; i++) {
        traverseFileTree(entries[i], files);
      }
    });
  }
};

// 格式化文件大小
const formatFileSize = (size) => {
  if (size < 1024) {
    return size + " B";
  } else if (size < 1024 * 1024) {
    return (size / 1024).toFixed(2) + " KB";
  } else {
    return (size / (1024 * 1024)).toFixed(2) + " MB";
  }
};

// 清空文件
const clearFiles = () => {
  selectedFiles.value = [];
  fileInput.value.value = null;
};

// 开始处理
const startProcessing = async () => {
  if (selectedFiles.value.length === 0) {
    ElMessage.warning("请先选择要处理的文件");
    return;
  }

  processing.value = true;
  uploadProgress.value = 0;
  errorMessage.value = "";

  try {
    // 准备FormData
    const formData = new FormData();
    selectedFiles.value.forEach((file) => {
      formData.append("files", file);
    });
    formData.append("model_type", "node"); // 默认使用node模型

    // 使用封装的API发送异步处理请求
    const response = await processHtmlAsync(formData, (progressEvent) => {
      uploadProgress.value = Math.round(
        (progressEvent.loaded / progressEvent.total) * 100
      );
    });

    if (response.data && response.data.task_id) {
      taskId.value = response.data.task_id;
      taskStatus.value = "processing";
      ElMessage.success("文件已上传，正在处理中");

      // 开始轮询检查任务状态
      startStatusCheck();
    } else {
      throw new Error("未返回有效的任务ID");
    }
  } catch (error) {
    console.error("处理请求失败:", error);
    processing.value = false;
    errorMessage.value = error.message || "提交处理请求时发生错误";
    taskStatus.value = "failed";
    ElMessage.error("请求失败: " + errorMessage.value);
  }
};

// 开始轮询检查任务状态
const startStatusCheck = () => {
  if (checkStatusInterval.value) {
    clearInterval(checkStatusInterval.value);
  }

  checkStatusInterval.value = setInterval(async () => {
    try {
      // 使用封装的API检查任务状态
      const response = await getTaskStatus(taskId.value);
      const data = response.data;

      taskStatus.value = data.status;

      if (data.status === "completed") {
        clearInterval(checkStatusInterval.value);
        processing.value = false;

        // 将结果保存到本地存储
        saveResultsToLocalStorage(data);

        ElMessage.success("处理完成！");
      } else if (data.status === "failed") {
        clearInterval(checkStatusInterval.value);
        processing.value = false;
        errorMessage.value = data.error || "处理失败";
        ElMessage.error("处理失败: " + errorMessage.value);
      }
    } catch (error) {
      console.error("检查任务状态失败:", error);
      // 如果连续几次检查失败，可能需要停止轮询
    }
  }, 3000); // 每3秒检查一次
};

// 将结果保存到本地存储
const saveResultsToLocalStorage = (data) => {
  try {
    // 获取当前存储的结果
    const storedResults = JSON.parse(
      localStorage.getItem("denoisedResults") || "[]"
    );

    // 为每个结果创建条目
    if (data.results && data.results.length > 0) {
      const timestamp = new Date().toLocaleString();

      const newResults = data.results.map((result, index) => {
        // 从文件名或内容中提取URL
        let url = result.filename;
        try {
          // 尝试从内容中提取标题作为URL
          const titleMatch = result.content.match(/<title>(.*?)<\/title>/i);
          if (titleMatch && titleMatch[1]) {
            url = titleMatch[1];
          }
        } catch (e) {
          console.error("提取URL失败:", e);
        }

        return {
          id: Date.now() + index,
          url: url,
          time: timestamp,
          content: result.content,
          task_id: taskId.value,
          selected: false,
        };
      });

      // 将新结果添加到存储中
      localStorage.setItem(
        "denoisedResults",
        JSON.stringify([...newResults, ...storedResults])
      );
    }
  } catch (error) {
    console.error("保存结果到本地存储失败:", error);
    ElMessage.warning("保存结果到本地失败，但您仍然可以下载结果");
  }
};

// 下载结果
const downloadResults = async () => {
  try {
    // 使用封装的API下载任务结果
    const response = await downloadTaskResults(taskId.value);

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `batch-denoised-${new Date().getTime()}.zip`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    ElMessage.success("下载成功");
  } catch (error) {
    console.error("下载结果失败:", error);
    ElMessage.error("下载结果失败: " + (error.message || "未知错误"));
  }
};

// 查看结果
const viewResults = () => {
  router.push("/results");
};

// 重置处理
const resetProcess = () => {
  processing.value = false;
  taskId.value = null;
  taskStatus.value = null;
  errorMessage.value = "";
  uploadProgress.value = 0;

  if (checkStatusInterval.value) {
    clearInterval(checkStatusInterval.value);
    checkStatusInterval.value = null;
  }
};

// 组件卸载时清除定时器
onUnmounted(() => {
  if (checkStatusInterval.value) {
    clearInterval(checkStatusInterval.value);
  }
});
</script>

<style scoped>
.multiple-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.title-section {
  margin-bottom: 2rem;
  text-align: center;
}

.title-section h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.title-section p {
  font-size: 1.2rem;
  color: #666;
}

.upload-section {
  margin-bottom: 2rem;
}

.upload-card {
  border: 2px dashed #ccc;
  border-radius: 8px;
  padding: 3rem;
  text-align: center;
  background-color: #f9f9f9;
  cursor: pointer;
  transition: all 0.3s;
}

.upload-card:hover {
  border-color: #1890ff;
  background-color: #f0f8ff;
}

.upload-icon {
  margin-bottom: 1rem;
  color: #1890ff;
}

.upload-text p {
  margin: 0.5rem 0;
  font-size: 1.2rem;
  color: #333;
}

.upload-hint {
  font-size: 0.9rem !important;
  color: #999 !important;
}

.file-list {
  margin-bottom: 2rem;
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.list-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.files {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.file-item {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-radius: 4px;
  background-color: #f5f5f5;
}

.file-item .el-icon {
  margin-right: 0.5rem;
  color: #1890ff;
}

.file-name {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-size {
  color: #999;
  font-size: 0.9rem;
  margin-left: 1rem;
}

.more-files {
  text-align: center;
  padding: 0.5rem;
  color: #999;
  font-style: italic;
}

.progress-section {
  margin-top: 2rem;
}

.progress-card {
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  text-align: center;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.progress-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
}

.uploading,
.processing,
.completed,
.failed {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.success-icon {
  color: #52c41a;
}

.error-icon {
  color: #f5222d;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
</style>
