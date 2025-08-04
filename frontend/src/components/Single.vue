<template>
  <div>
    <div class="input-section">
      <h3 style="color: black; font-weight: 400">选择输入方式</h3>

      <!-- 输入方式选择 -->
      <div class="input-type-selector">
        <div class="radio-group">
          <label class="radio-button" :class="{ active: inputType === 'file' }">
            <input
              type="radio"
              value="file"
              v-model="inputType"
              name="inputType"
            />
            <el-icon class="radio-icon"><Upload /></el-icon>
            <span class="radio-label">上传HTML文件</span>
          </label>
          <label class="radio-button" :class="{ active: inputType === 'url' }">
            <input
              type="radio"
              value="url"
              v-model="inputType"
              name="inputType"
            />
            <el-icon class="radio-icon"><i-ep-link /></el-icon>
            <span class="radio-label">输入网址URL</span>
          </label>
        </div>
      </div>

      <!-- 文件上传区域 -->
      <div v-if="inputType === 'file'" class="file-upload-wrapper">
        <div class="file-upload">
          <input
            type="file"
            accept=".html,.htm"
            multiple
            ref="fileInput"
            @change="handleFileChange"
            class="file-input"
          />
          <div class="upload-interface">
            <el-icon style="font-size: 24px"><Upload /></el-icon>
            <span>点击或拖拽HTML文件到此处</span>
            <span class="file-count" v-if="selectedFiles.length > 0">
              已选择 {{ selectedFiles.length }} 个文件
            </span>
          </div>
        </div>
        <button
          @click="processFiles"
          :disabled="isProcessing || !selectedFiles.length"
        >
          {{ isProcessing ? "处理中..." : "开始处理" }}
        </button>
      </div>

      <!-- URL输入区域 -->
      <div v-if="inputType === 'url'" class="url-input-wrapper">
        <el-input
          v-model="inputUrl"
          placeholder="请输入网址 (例如: https://www.example.com)"
          :disabled="isProcessing"
          @keyup.enter="processWebUrl"
          class="url-input"
        >
          <template #prefix>
            <el-icon><i-ep-link /></el-icon>
          </template>
        </el-input>
        <button @click="processWebUrl" :disabled="isProcessing || !inputUrl">
          {{ isProcessing ? "处理中..." : "开始处理" }}
        </button>
      </div>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
    </div>
    <div class="choose-section" style="padding: 1rem">
      <el-tabs v-model="activeName" class="demo-tabs">
        <el-tab-pane label="Preview" name="first">
          <div class="preview-section">
            <h2 class="preview-title">
              <el-icon><Document /></el-icon>
              预览文件内容
            </h2>
            <!-- From Uiverse.io by Bastiennnn -->
            <div class="card" v-if="currentPreview">
              <div class="header">
                <div class="top">
                  <div class="circle">
                    <span class="red circle2"></span>
                  </div>
                  <div class="circle">
                    <span class="yellow circle2"></span>
                  </div>
                  <div class="circle">
                    <span class="green circle2"></span>
                  </div>
                  <div class="title">
                    <p id="title2">{{ currentFileName }}</p>
                  </div>
                </div>
              </div>
              <div class="code-container">
                <div
                  class="area"
                  id="code"
                  name="code"
                  v-html="htmlContent"
                ></div>
              </div>
            </div>
            <div class="no-files" v-else>请选择HTML文件以查看预览</div>
          </div>
        </el-tab-pane>
        <!-- <el-tab-pane label="Set" name="second">
          <div class="set">
            <div class="tag-choose">
              <span>包含网页标签</span>
              <el-input
                v-model="includeTags"
                style="width: 240px"
                placeholder="span,.set,#header"
              />
              <span>忽略网页标签</span>
              <el-input
                v-model="excludeTags"
                style="width: 240px"
                placeholder="span,.set,#header"
              />
            </div>
            <div class="checked-box" style="margin-top: 25px">
              <label class="container">
                <input v-model="includeHtml" type="checkbox" />
                <div class="checkmark"></div>
                <span>包括HTML内容</span>
              </label>
              <label class="container">
                <input v-model="includeLinks" type="checkbox" />
                <div class="checkmark"></div>
                <span>包含页面链接</span>
              </label>
            </div>
            <span class="explain">
              <el-icon><Pointer /></el-icon>选项详情请查看说明文档Docs
            </span>
          </div>
        </el-tab-pane> -->
      </el-tabs>
    </div>
    <div class="progress-section" v-if="isProcessing">
      <img src="@/assets/bean.gif" style="display: block; margin: 0 auto" />
      <div class="progress-info">
        <span class="progress-percentage">{{ progress }}%</span>
      </div>
      <div class="progress-bar">
        <div class="progress" :style="{ width: progress + '%' }"></div>
      </div>
    </div>
    <div
      class="progress-section"
      v-if="isShowJump"
      style="display: flex; justify-content: space-around"
    >
      <router-link to="/results" class="nav-item">
        <button>查看结果</button>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import {
  Document,
  Pointer,
  Upload,
  Link as IEpLink,
} from "@element-plus/icons-vue";
import axios from "axios";
import { ElMessage } from "element-plus";
// 导入封装的API
import {
  processHtmlSync,
  getTaskStatus,
  downloadTaskResults,
  fetchHtmlFromUrl,
  processUrl,
} from "@/api/html_local";

const htmlContent = ref("");
const activeName = ref("first");
const progress = ref(0);
const isProcessing = ref(false);
const isShowJump = ref(false);
const errorMessage = ref("");
const currentFileName = ref("");
const taskId = ref(null);
const currentPreview = ref(false);

// 输入方式切换
const inputType = ref("file");
const inputUrl = ref("");

// 清洗配置选项
const includeTags = ref("");
const excludeTags = ref("");
const includeHtml = ref(true);
const includeLinks = ref(true);

// 文件相关
const fileInput = ref(null);
const selectedFiles = ref([]);

onMounted(() => {
  // 初始化示例，后续可以删除
  // htmlContent.value = exampleContent;
});

const handleFileChange = (event) => {
  selectedFiles.value = Array.from(event.target.files);
  if (selectedFiles.value.length > 0) {
    // 显示第一个文件的预览
    const file = selectedFiles.value[0];
    currentFileName.value = file.name;

    const reader = new FileReader();
    reader.onload = (e) => {
      htmlContent.value = e.target.result;
      currentPreview.value = true;
    };
    reader.readAsText(file);
  } else {
    currentPreview.value = false;
    htmlContent.value = "";
    currentFileName.value = "";
  }
};

const processFiles = async () => {
  if (selectedFiles.value.length === 0) {
    errorMessage.value = "请选择至少一个HTML文件";
    return;
  }

  try {
    errorMessage.value = "";
    isProcessing.value = true;
    progress.value = 0;

    // 设置进度模拟
    const progressInterval = setInterval(() => {
      if (progress.value < 90) {
        progress.value += 5;
      }
    }, 500);

    // 构建FormData
    const formData = new FormData();
    selectedFiles.value.forEach((file) => {
      formData.append("files", file);
    });

    // 添加配置选项
    // 如果有标签配置，创建tag_probs文件
    if (includeTags.value || excludeTags.value) {
      const tagProbs = {
        include_tags: includeTags.value
          ? includeTags.value.split(",").map((t) => t.trim())
          : [],
        exclude_tags: excludeTags.value
          ? excludeTags.value.split(",").map((t) => t.trim())
          : [],
        include_html: includeHtml.value,
        include_links: includeLinks.value,
      };

      const tagProbsBlob = new Blob([JSON.stringify(tagProbs)], {
        type: "application/json",
      });
      formData.append("tag_probs", tagProbsBlob, "tag_config.json");
    }

    formData.append("model_type", "node"); // 使用默认模型类型

    // 使用封装后的API调用
    const response = await processHtmlSync(formData);

    // 清除进度条间隔
    clearInterval(progressInterval);

    if (response.data && response.data.status === "completed") {
      // 处理成功
      progress.value = 100;

      // 保存任务ID以便在Results页面使用
      if (response.data.task_id) {
        taskId.value = response.data.task_id;

        try {
          // 使用封装后的API下载处理结果的ZIP文件
          const downloadResponse = await downloadTaskResults(
            response.data.task_id
          );

          // 创建文件下载链接
          const url = window.URL.createObjectURL(
            new Blob([downloadResponse.data])
          );
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute(
            "download",
            `denoised-content-${new Date().getTime()}.zip`
          );
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);

          // 从任务详情API获取处理后的内容
          let resultContent = "";
          let taskDetail = null;

          try {
            // 使用封装后的API获取任务详情
            const taskResponse = await getTaskStatus(response.data.task_id);

            taskDetail = taskResponse.data;

            // 如果任务详情中有结果
            if (
              taskDetail &&
              taskDetail.results &&
              taskDetail.results.length > 0
            ) {
              resultContent = taskDetail.results[0].content;
            } else {
              // 如果任务详情中没有结果，尝试使用单独的结果API
              const resultResponse = await getTaskStatus(response.data.task_id);

              if (resultResponse.data && resultResponse.data.length > 0) {
                resultContent = resultResponse.data[0].content;
              } else {
                // 如果API都没有返回结果，使用原始HTML作为备选
                resultContent = htmlContent.value;
                console.warn("未能从API获取处理结果，使用原始HTML作为备选");
              }
            }
          } catch (apiError) {
            console.error("获取任务详情失败:", apiError);
            // 如果API请求失败，使用原始结果
            resultContent =
              response.data.results && response.data.results.length > 0
                ? response.data.results[0].content
                : htmlContent.value;
          }

          // 提取标题
          let title = currentFileName.value || "本地HTML文件";
          try {
            const titleMatch = resultContent.match(/<title>(.*?)<\/title>/i);
            if (titleMatch && titleMatch[1]) {
              title = titleMatch[1];
            } else {
              const h1Match = resultContent.match(/<h1>(.*?)<\/h1>/i);
              if (h1Match && h1Match[1]) {
                title = h1Match[1];
              }
            }
          } catch (e) {
            console.error("提取标题失败:", e);
          }

          // 保存处理结果信息到本地存储，供Results页面使用
          const resultItem = {
            id: new Date().getTime(),
            url: title,
            time: new Date().toLocaleString(),
            task_id: response.data.task_id,
            content: resultContent,
            selected: false,
            isBatch: false, // 明确标记为非批量结果
            filename: currentFileName.value, // 和批量处理保持一致的字段名
          };

          // 调试输出，确认内容正确
          console.log("保存的内容:", {
            contentSource: "tasks API",
            contentPreview: resultContent.substring(0, 100),
            title,
            filename: currentFileName.value,
          });

          // 获取之前的结果列表
          const existingResults = JSON.parse(
            localStorage.getItem("denoisedResults") || "[]"
          );
          // 添加新结果
          existingResults.push(resultItem);
          // 存储更新后的结果列表
          localStorage.setItem(
            "denoisedResults",
            JSON.stringify(existingResults)
          );
          localStorage.setItem("lastTaskId", response.data.task_id);
        } catch (downloadError) {
          console.error("下载结果文件失败:", downloadError);
          ElMessage.warning(
            "处理成功，但下载结果文件失败，可以稍后在结果页面重试"
          );
        }
      }

      setTimeout(() => {
        isShowJump.value = true;
        isProcessing.value = false;
      }, 1000);

      ElMessage({
        message: `成功处理 ${
          response.data.result_count || selectedFiles.value.length
        } 个文件`,
        type: "success",
      });

      // 重置文件选择
      if (fileInput.value) {
        fileInput.value.value = null;
      }
      selectedFiles.value = [];
    } else {
      // 处理失败
      handleError("处理失败：" + (response.data.error || "未知错误"));
    }
  } catch (error) {
    handleError(error);
  }
};

// 处理URL输入
const processWebUrl = async () => {
  if (!inputUrl.value) {
    errorMessage.value = "请输入有效的URL";
    return;
  }

  try {
    errorMessage.value = "";
    isProcessing.value = true;
    progress.value = 0;
    currentPreview.value = false;

    // 设置进度模拟
    const progressInterval = setInterval(() => {
      if (progress.value < 90) {
        progress.value += 3;
      }
    }, 500);

    // 使用新的直接处理URL的API
    const response = await processUrl(inputUrl.value, "node");

    // 清除进度条间隔
    clearInterval(progressInterval);

    if (response.data && response.data.status === "completed") {
      // 处理成功
      progress.value = 100;

      // 从响应中获取任务ID、标题和结果
      const responseTaskId = response.data.task_id;
      const pageTitle = response.data.title || "";
      taskId.value = responseTaskId;

      try {
        // 下载处理结果
        const downloadResponse = await downloadTaskResults(responseTaskId);

        // 创建文件下载链接
        const url = window.URL.createObjectURL(
          new Blob([downloadResponse.data])
        );
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute(
          "download",
          `denoised-content-${new Date().getTime()}.zip`
        );
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        // 获取结果内容
        let resultContent = "";

        // 如果API直接返回了结果内容
        if (response.data.results && response.data.results.length > 0) {
          resultContent = response.data.results[0].content;

          // 显示获取到的处理后的HTML预览
          htmlContent.value = resultContent;
          currentFileName.value = pageTitle || new URL(inputUrl.value).hostname;
          currentPreview.value = true;
        } else {
          // 如果没有直接返回结果，尝试从任务API获取
          try {
            const taskResponse = await getTaskStatus(responseTaskId);
            const taskDetail = taskResponse.data;

            if (
              taskDetail &&
              taskDetail.results &&
              taskDetail.results.length > 0
            ) {
              resultContent = taskDetail.results[0].content;

              // 显示获取到的处理后的HTML预览
              htmlContent.value = resultContent;
              currentFileName.value =
                pageTitle || new URL(inputUrl.value).hostname;
              currentPreview.value = true;
            } else {
              // 如果任务详情中没有结果，尝试使用单独的结果API
              const resultResponse = await getTaskStatus(responseTaskId);

              if (resultResponse.data && resultResponse.data.length > 0) {
                resultContent = resultResponse.data[0].content;

                // 显示获取到的处理后的HTML预览
                htmlContent.value = resultContent;
                currentFileName.value =
                  pageTitle || new URL(inputUrl.value).hostname;
                currentPreview.value = true;
              } else {
                console.warn("未能从API获取处理结果");
              }
            }
          } catch (apiError) {
            console.error("获取任务详情失败:", apiError);
          }
        }

        // 提取标题
        let title = pageTitle || inputUrl.value;
        if (!title && resultContent) {
          try {
            const titleMatch = resultContent.match(/<title>(.*?)<\/title>/i);
            if (titleMatch && titleMatch[1]) {
              title = titleMatch[1];
            } else {
              const h1Match = resultContent.match(/<h1>(.*?)<\/h1>/i);
              if (h1Match && h1Match[1]) {
                title = h1Match[1];
              }
            }
          } catch (e) {
            console.error("提取标题失败:", e);
          }
        }

        // 保存处理结果信息到本地存储，供Results页面使用
        const resultItem = {
          id: new Date().getTime(),
          url: title,
          time: new Date().toLocaleString(),
          task_id: responseTaskId,
          content: resultContent,
          selected: false,
          isBatch: false,
          filename: currentFileName.value,
          source_url: inputUrl.value,
        };

        // 获取之前的结果列表
        const existingResults = JSON.parse(
          localStorage.getItem("denoisedResults") || "[]"
        );
        // 添加新结果
        existingResults.push(resultItem);
        // 存储更新后的结果列表
        localStorage.setItem(
          "denoisedResults",
          JSON.stringify(existingResults)
        );
        localStorage.setItem("lastTaskId", responseTaskId);
      } catch (downloadError) {
        console.error("下载结果文件失败:", downloadError);
        ElMessage.warning(
          "处理成功，但下载结果文件失败，可以稍后在结果页面重试"
        );
      }

      setTimeout(() => {
        isShowJump.value = true;
        isProcessing.value = false;
      }, 1000);

      ElMessage({
        message: `成功处理 URL: ${inputUrl.value}`,
        type: "success",
      });

      // 重置URL输入
      inputUrl.value = "";
    } else {
      // 处理失败
      handleError(
        "处理失败：" +
          (response.data?.message || response.data?.error || "未知错误")
      );
    }
  } catch (error) {
    handleError(error);
  }
};

const handleError = (error) => {
  console.error("处理文件时出错:", error);
  isProcessing.value = false;
  progress.value = 0;

  if (error.response) {
    errorMessage.value = `请求错误 (${error.response.status}): ${
      error.response.data.error || error.response.data.message || "服务器错误"
    }`;
  } else if (error.request) {
    errorMessage.value = "无法连接到服务器，请确认API服务是否正在运行";
  } else {
    errorMessage.value = error.message || "处理请求时出错";
  }

  ElMessage({
    message: errorMessage.value,
    type: "error",
  });
};
</script>

<style scoped>
.explain {
  color: #727070;
  margin-left: auto;
  font-size: small;
}
.explain:hover {
  color: #1a1919;
  cursor: pointer;
  text-decoration: underline;
}
.explain .el-icon {
  margin-right: 5px;
}
.set {
  display: flex;
}
.tag-choose {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  border-right: 3px solid #a1a3a3d8;
  padding-right: 50px;
  margin-right: 50px;
}
.tag-choose span {
  color: #5e5d5d;
  font-weight: 600;
  margin-bottom: 5px;
  margin-top: 10px;
}
.checked-box {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
}

.input-section {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
}

.file-upload-wrapper {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.file-upload {
  position: relative;
  flex: 1;
  height: 120px;
  border: 2px dashed rgba(76, 201, 240, 0.3);
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  transition: all 0.3s ease;
}

.file-upload:hover {
  border-color: #4cc9f0;
  box-shadow: 0 0 15px rgba(76, 201, 240, 0.3);
}

.file-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
  z-index: 10;
}

.upload-interface {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #676464;
}

.upload-interface span {
  margin-top: 10px;
}

.file-count {
  color: #4cc9f0;
  font-weight: bold;
}

.no-files {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  color: #999;
  background: #f9f9f9;
  border-radius: 8px;
}

.progress-section {
  padding: 1rem;
  background: rgb(255, 255, 255);
  border-radius: 12px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.progress-percentage {
  color: #4cc9f0;
  font-size: 0.9rem;
}

.progress-bar {
  height: 8px;
  background: rgb(137, 135, 135);
  border-radius: 4px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: linear-gradient(90deg, #4ade80, #3bcc65);
  border-radius: 4px;
  transition: width 0.3s ease;
}

/* From Uiverse.io by Bastiennnn */
button {
  transform: translateY(-8px);
  padding: 10px 24px;
  border-radius: 12px;
  border: 0;
  background-color: #4ade80;
  letter-spacing: 1.5px;
  font-size: 14px;
  font-weight: 700;
  transition: all 0.3s ease;
  box-shadow: #3bcc65 0px 10px 0px 0px;
  color: white;
  cursor: pointer;
}

button:hover {
  box-shadow: #3bcc65 0px 7px 0px 0px;
  transform: translateY(-5px);
}

button:active {
  background-color: #4ade80;
  box-shadow: #3bcc65 0px 0px 0px 0px;
  transform: translateY(0px);
  transition: 200ms;
}

button:disabled {
  background-color: #95d5a7;
  box-shadow: #95d5a7 0px 7px 0px 0px;
  cursor: not-allowed;
}

.preview-section {
  margin-bottom: 5px;
}

.preview-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #323131;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  padding-left: 0.5rem;
  position: relative;
}

.preview-title::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 70%;
  background: linear-gradient(to bottom, #4ade80, #3bcc65);
  border-radius: 2px;
}

.preview-title .el-icon {
  color: #4ade80;
  font-size: 1.3rem;
}

/* From Uiverse.io by Bastiennnn */
.card {
  width: 100%;
  max-width: 1100px;
  height: 500px;
  background-color: #ffffff;
  border-radius: 12px;
  z-index: 1;
  box-shadow: 0px 8px 20px rgba(74, 222, 128, 0.15);
  transition: 0.4s;
  margin-bottom: 10px;
  padding-left: 10px;
  padding-right: 10px;
}

.card:hover {
  transform: translateY(-7px);
  box-shadow: 0px 12px 25px rgba(74, 222, 128, 0.25);
}

.top {
  display: flex;
  align-items: center;
  padding-left: 10px;
}

.circle {
  padding: 0 4px;
}

.circle2 {
  display: inline-block;
  align-items: center;
  width: 10px;
  height: 10px;
  padding: 1px;
  border-radius: 5px;
}

.red {
  background-color: #ff605c;
}

.yellow {
  background-color: #ffbd44;
}

.green {
  background-color: #00ca4e;
}

.header {
  margin: 5px;
  margin-top: 5px;
  border-radius: 5px;
}

#title2 {
  color: rgb(89, 89, 89);
  font-size: 15px;
  font-weight: 700;
  margin-left: 10px;
  margin-top: 15px;
}

.code-container {
  text-align: center;
}
#code {
  width: 100%;
  height: 430px;
  background-color: #ffffff;
  border-radius: 5px;
  border: 1px solid #e0e0e0;
  color: #333333;
  padding: 15px;
  overflow: auto;
  font-family: "Consolas", "Monaco", monospace;
  font-size: 14px;
  line-height: 1.5;
  text-align: left;
}

#code :deep(*) {
  font-family: inherit;
  color: inherit;
}

/* From Uiverse.io by andrew-demchenk0 */
.container {
  --input-focus: #2d8cf0;
  --input-out-of-focus: #ccc;
  --bg-color: #fff;
  --bg-color-alt: #666;
  --main-color: #323232;
  position: relative;
  cursor: pointer;
}

.container input {
  position: absolute;
  opacity: 0;
}

.container span {
  color: #5e5d5d;
  font-weight: 500;
  position: relative;
  top: -17px;
  left: 23px;
}
.checkmark {
  width: 15px;
  height: 15px;
  position: relative;
  top: 0;
  left: 0;
  border: 1px solid var(--main-color);
  border-radius: 5px;
  box-shadow: 2px 2px var(--main-color);
  background-color: var(--input-out-of-focus);
  transition: all 0.3s;
}

.container input:checked ~ .checkmark {
  background-color: var(--input-focus);
}

.checkmark:after {
  content: "";
  width: 3.5px;
  height: 7.5px;
  position: absolute;
  top: 1px;
  left: 4px;
  display: none;
  border: solid var(--bg-color);
  border-width: 0 2.5px 2.5px 0;
  transform: rotate(45deg);
}

.container input:checked ~ .checkmark:after {
  display: block;
}

.error-message {
  color: #ff4d4f;
  margin-top: 8px;
  font-size: 14px;
}

/* 优化后的输入方式选择器样式 */
.input-type-selector {
  margin: 20px 0;
}

.radio-group {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.radio-button {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  background-color: #f5f7fa;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.radio-button.active {
  background-color: #ecf5ff;
  border-color: #409eff;
  color: #409eff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.radio-button input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.radio-icon {
  margin-right: 8px;
  font-size: 18px;
  color: #606266;
}

.radio-button.active .radio-icon {
  color: #409eff;
}

.radio-label {
  color: #606266;
  font-weight: 500;
  font-size: 15px;
}

.radio-button.active .radio-label {
  color: #409eff;
}

.url-input-wrapper {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 10px;
}

.url-input {
  flex: 1;
  max-width: 800px;
}

/* 修复URL输入框文字颜色 */
:deep(.el-input__inner) {
  color: #606266 !important; /* 使用深灰色作为输入文本颜色 */
}

:deep(.el-input__wrapper) {
  background-color: #fff !important; /* 确保输入框背景为白色 */
}

:deep(.el-input__prefix) {
  color: #409eff; /* 设置前缀图标颜色 */
}
</style>
