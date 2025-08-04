<template>
  <div class="results-page">
    <Sidebar />
    <div class="main-content">
      <div class="results-header">
        <h1>RESULTS</h1>
        <div class="header-content">
          <h2>查看网页清洗结果并导出供LLM使用的数据</h2>
          <div class="batch-actions">
            <button
              class="cssbuttons-io"
              @click="exportResults"
              :disabled="!selectedResults.length"
            >
              <span
                ><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path d="M0 0h24v24H0z" fill="none"></path>
                  <path
                    d="M24 12l-5.657 5.657-1.414-1.414L21.172 12l-4.243-4.243 1.414-1.414L24 12zM2.828 12l4.243 4.243-1.414 1.414L0 12l5.657-5.657L7.07 7.757 2.828 12zm6.96 9H7.66l6.552-18h2.128L9.788 21z"
                    fill="currentColor"
                  ></path>
                </svg>
                批量导出</span
              >
            </button>
            <button
              :disabled="!selectedResults.length"
              @click="confirmBatchDelete"
              class="deletebutton"
            >
              删除
            </button>
          </div>
        </div>

        <div class="search-and-format">
          <div class="search-box">
            <el-input
              v-model="searchQuery"
              placeholder="搜索结果..."
              prefix-icon="Search"
              clearable
            />
          </div>

          <div class="date-picker">
            <span class="date-label">按日期筛选：</span>
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY/MM/DD"
              value-format="YYYY-MM-DD"
              :clearable="true"
              @change="onDateRangeChange"
            />
          </div>

          <div class="type">
            <div class="tag">
              <img src="@/assets/set.png" class="deepseek" />导出格式
            </div>
            <el-radio-group v-model="radio" style="display: inline-block">
              <el-radio :label="3">XML</el-radio>
              <el-radio :label="6">JSON</el-radio>
            </el-radio-group>
          </div>
        </div>
      </div>

      <div class="results-list">
        <div v-if="filteredResults.length === 0" class="no-results">
          {{ searchQuery ? "没有匹配的搜索结果" : "暂无处理结果" }}
        </div>
        <div v-else class="result-items">
          <!-- 单个结果项 -->
          <div
            v-for="result in filteredResults"
            :key="result.id"
            class="result-item"
            @click="viewResult(result)"
            :class="{ 'batch-item': result.isBatch }"
          >
            <div class="result-info">
              <el-checkbox
                v-model="result.selected"
                @click.stop
                class="result-checkbox"
              />
              <div class="result-details">
                <div class="result-title-row">
                  <h3 class="url">{{ result.url }}</h3>
                  <el-tag size="small" v-if="result.isBatch" type="success"
                    >批量</el-tag
                  >
                </div>
                <div class="result-meta">
                  <span class="time">
                    <el-icon><Calendar /></el-icon>
                    {{ result.time }}
                  </span>
                  <span class="file-count" v-if="result.isBatch">
                    <el-icon><Document /></el-icon>
                    {{ result.fileCount }}个文件
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 查看结果对话框 -->
    <ElDialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="70%"
      class="result-dialog"
    >
      <!-- 批量结果展示 -->
      <template v-if="currentResult?.isBatch">
        <div class="batch-controls">
          <div class="batch-search">
            <el-input
              v-model="batchSearchQuery"
              placeholder="在批量结果中搜索..."
              prefix-icon="Search"
              clearable
            />
          </div>
          <div class="batch-navigation">
            <span
              >当前查看: {{ currentBatchIndex + 1 }}/{{
                filteredBatchResults.length
              }}</span
            >
            <div class="navigation-controls">
              <el-button
                size="small"
                :disabled="currentBatchIndex === 0"
                @click="currentBatchIndex--"
              >
                上一个
              </el-button>
              <el-button
                size="small"
                :disabled="currentBatchIndex >= filteredBatchResults.length - 1"
                @click="currentBatchIndex++"
              >
                下一个
              </el-button>
            </div>
          </div>
        </div>

        <div v-if="filteredBatchResults.length === 0" class="no-batch-results">
          没有匹配的搜索结果
        </div>
        <div v-else class="batch-content">
          <div class="batch-file-info">
            <h4>{{ getCurrentBatchItem?.filename || "未命名文件" }}</h4>
          </div>
          <div class="dialog-tabs">
            <div class="tab-buttons">
              <button
                class="tab-button"
                :class="{ active: radio === 3 }"
                @click="radio = 3"
              >
                XML
              </button>
              <button
                class="tab-button"
                :class="{ active: radio === 6 }"
                @click="radio = 6"
              >
                JSON
              </button>
            </div>
          </div>
          <div class="preview-section">
            <h2 class="preview-title">
              <el-icon><Document /></el-icon>
              {{ radio === 3 ? "XML格式" : "JSON格式" }}
            </h2>
            <div class="result-content">
              <pre
                v-if="getCurrentBatchItem && radio === 3"
                class="code-block"
                >{{ convertToXml(getCurrentBatchItem) }}</pre
              >
              <pre
                v-if="getCurrentBatchItem && radio === 6"
                class="code-block"
                >{{ convertToJson(getCurrentBatchItem) }}</pre
              >
            </div>
          </div>
        </div>
      </template>

      <!-- 单个结果展示 -->
      <template v-else>
        <div class="dialog-tabs">
          <div class="tab-buttons">
            <button
              class="tab-button"
              :class="{ active: radio === 3 }"
              @click="radio = 3"
            >
              XML
            </button>
            <button
              class="tab-button"
              :class="{ active: radio === 6 }"
              @click="radio = 6"
            >
              JSON
            </button>
          </div>
        </div>
        <div class="preview-section">
          <h2 class="preview-title">
            <el-icon><Document /></el-icon>
            {{ radio === 3 ? "XML格式" : "JSON格式" }}
          </h2>
          <div class="result-content">
            <pre v-if="currentResult && radio === 3" class="code-block">{{
              convertToXml(currentResult)
            }}</pre>
            <pre v-if="currentResult && radio === 6" class="code-block">{{
              convertToJson(currentResult)
            }}</pre>
          </div>
        </div>
      </template>

      <template #footer>
        <span class="dialog-footer">
          <button class="copybutton" @click="copyContent">复制</button>
          <button
            v-if="currentResult?.isBatch"
            class="downloadbutton"
            @click="downloadBatchResults"
          >
            下载ZIP
          </button>
        </span>
      </template>
    </ElDialog>

    <!-- 删除确认对话框 -->
    <ElDialog
      v-model="deleteDialogVisible"
      title="确认删除"
      width="30%"
      class="delete-dialog"
    >
      <div class="delete-content">确定要删除选中的记录吗？此操作不可恢复。</div>
      <template #footer>
        <span class="dialog-footer">
          <ElButton @click="deleteDialogVisible = false" type="primary"
            >取消</ElButton
          >
          <ElButton type="danger" @click="deleteResult">确定</ElButton>
        </span>
      </template>
    </ElDialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { Document, Calendar, Search } from "@element-plus/icons-vue";
import {
  ElButton,
  ElDialog,
  ElCheckbox,
  ElMessage,
  ElInput,
  ElTag,
} from "element-plus";
import Sidebar from "@/components/Sidebar.vue";
import axios from "axios";

const radio = ref(3);
const results = ref([]);
const dialogVisible = ref(false);
const deleteDialogVisible = ref(false);
const currentResult = ref(null);
const searchQuery = ref("");
const batchSearchQuery = ref("");
const currentBatchIndex = ref(0);
const dateRange = ref([]);

// 从本地存储加载已处理结果
onMounted(() => {
  loadResultsFromStorage();
});

const loadResultsFromStorage = () => {
  try {
    const storedResults = JSON.parse(
      localStorage.getItem("denoisedResults") || "[]"
    );

    if (storedResults && storedResults.length) {
      // 处理批量结果
      const groupedResults = {};
      const singleResults = [];

      // 将具有相同task_id的结果分组
      storedResults.forEach((result) => {
        // 检查是否明确标记为非批量结果
        if (result.isBatch === false) {
          // 明确标记为单个结果的情况
          singleResults.push({ ...result, isBatch: false });
        } else if (result.task_id && !result.hasOwnProperty("isBatch")) {
          // 有task_id且未明确标记为非批量结果，视为批量结果
          if (!groupedResults[result.task_id]) {
            groupedResults[result.task_id] = {
              id: result.task_id,
              task_id: result.task_id,
              url: `批量结果 (${new Date(result.time).toLocaleDateString()})`,
              time: result.time,
              isBatch: true,
              selected: false,
              items: [],
              fileCount: 0,
            };
          }
          groupedResults[result.task_id].items.push(result);
          groupedResults[result.task_id].fileCount++;
        } else {
          // 没有task_id或旧数据，视为单个结果
          singleResults.push({ ...result, isBatch: false });
        }
      });

      // 将结果合并并按时间排序（从新到旧）
      const allResults = [...Object.values(groupedResults), ...singleResults];

      // 按时间从新到旧排序
      allResults.sort((a, b) => {
        // 转换时间字符串为时间戳进行比较
        const timeA = new Date(a.time).getTime();
        const timeB = new Date(b.time).getTime();
        return timeB - timeA; // 降序排序（从新到旧）
      });

      results.value = allResults;
    }
  } catch (error) {
    console.error("加载存储的结果失败:", error);
    ElMessage.error("加载存储的结果失败");
  }
};

// 搜索功能
const filteredResults = computed(() => {
  if (!searchQuery.value && !dateRange.value.length) return results.value;

  const query = searchQuery.value.toLowerCase();

  return results.value.filter((result) => {
    const isQueryMatch =
      result.url.toLowerCase().includes(query) ||
      (result.content && result.content.toLowerCase().includes(query));

    const isDateMatch = dateRange.value.length
      ? new Date(result.time) >= new Date(dateRange.value[0]) &&
        new Date(result.time) <= new Date(dateRange.value[1])
      : true;

    // 对于批量结果，搜索其中的内容
    if (result.isBatch) {
      return (
        isDateMatch &&
        (isQueryMatch ||
          result.items.some(
            (item) =>
              item.url.toLowerCase().includes(query) ||
              (item.content && item.content.toLowerCase().includes(query))
          ))
      );
    }

    // 对于单个结果
    return isDateMatch && isQueryMatch;
  });
});

// 批量结果内部搜索
const filteredBatchResults = computed(() => {
  if (!currentResult.value?.items) return [];

  if (!batchSearchQuery.value) return currentResult.value.items;

  const query = batchSearchQuery.value.toLowerCase();

  return currentResult.value.items.filter((item) => {
    return (
      item.url.toLowerCase().includes(query) ||
      (item.content && item.content.toLowerCase().includes(query)) ||
      (item.filename && item.filename.toLowerCase().includes(query))
    );
  });
});

// 当前查看的批量结果项
const getCurrentBatchItem = computed(() => {
  if (!filteredBatchResults.value.length) return null;

  // 确保索引在有效范围内
  if (currentBatchIndex.value >= filteredBatchResults.value.length) {
    currentBatchIndex.value = filteredBatchResults.value.length - 1;
  }

  return filteredBatchResults.value[currentBatchIndex.value];
});

// 当批量搜索查询变化时重置索引
watch(batchSearchQuery, () => {
  currentBatchIndex.value = 0;
});

const dialogTitle = computed(() => {
  if (!currentResult.value) return "";

  if (currentResult.value.isBatch) {
    return `批量结果 (${currentResult.value.fileCount}个文件)`;
  }

  return currentResult.value.url;
});

const selectedResults = computed(() => {
  return results.value.filter((result) => result.selected);
});

const viewResult = (result) => {
  currentResult.value = result;
  currentBatchIndex.value = 0; // 重置批量结果索引
  batchSearchQuery.value = ""; // 清空批量搜索
  dialogVisible.value = true;
};

const confirmBatchDelete = () => {
  if (selectedResults.value.length > 0) {
    deleteDialogVisible.value = true;
  }
};

const deleteResult = async () => {
  try {
    // 尝试从服务器删除任务
    for (const result of selectedResults.value) {
      if (result.task_id) {
        try {
          await axios.delete(
            `http://localhost:8001/api/tasks/${result.task_id}`
          );
        } catch (error) {
          console.warn(`删除服务器任务 ${result.task_id} 失败:`, error);
        }
      }
    }

    // 从本地列表中移除选中的结果
    const deletedResultIds = selectedResults.value.map((r) => r.id);
    results.value = results.value.filter(
      (result) => !deletedResultIds.includes(result.id)
    );

    // 更新本地存储
    const storedResults = JSON.parse(
      localStorage.getItem("denoisedResults") || "[]"
    );
    const newStoredResults = storedResults.filter((result) => {
      // 如果是批量结果的一部分，且该批量被删除
      if (selectedResults.value.some((s) => s.task_id === result.task_id)) {
        return false;
      }
      // 如果是单个结果，检查ID
      return !deletedResultIds.includes(result.id);
    });
    localStorage.setItem("denoisedResults", JSON.stringify(newStoredResults));

    deleteDialogVisible.value = false;
    ElMessage.success("删除成功");
  } catch (error) {
    console.error("删除任务失败:", error);
    ElMessage.error("删除部分任务失败");
  }
};

const exportResults = () => {
  if (selectedResults.value.length === 0) {
    return;
  }

  const exportFormat = radio.value === 3 ? "xml" : "json";

  selectedResults.value.forEach((result) => {
    if (result.isBatch) {
      // 如果是批量结果，创建一个ZIP文件
      exportBatchResult(result, exportFormat);
    } else {
      // 如果是单个结果，直接导出
      exportSingleResult(result, exportFormat);
    }
  });

  ElMessage.success(
    `已导出 ${
      selectedResults.value.length
    } 个结果为 ${exportFormat.toUpperCase()} 格式`
  );
};

// 导出单个结果
const exportSingleResult = (result, exportFormat) => {
  let content, filename, type;

  if (exportFormat === "xml") {
    content = convertToXml(result);
    filename = `article_${result.id}.xml`;
    type = "application/xml";
  } else {
    content = convertToJson(result);
    filename = `article_${result.id}.json`;
    type = "application/json";
  }

  // 创建下载链接
  const blob = new Blob([content], { type });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

// 导出批量结果（需要使用ZIP库，这里用简单方法替代）
const exportBatchResult = (result, exportFormat) => {
  if (!result.items || result.items.length === 0) {
    ElMessage.warning("批量结果中没有可导出的内容");
    return;
  }

  // 简单实现：逐个导出批量结果中的每个文件
  result.items.forEach((item, index) => {
    let content, filename, type;

    if (exportFormat === "xml") {
      content = convertToXml(item);
      filename = `${result.task_id}_${index}.xml`;
      type = "application/xml";
    } else {
      content = convertToJson(item);
      filename = `${result.task_id}_${index}.json`;
      type = "application/json";
    }

    // 创建下载链接
    const blob = new Blob([content], { type });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  });
};

// 下载批量结果的ZIP文件
const downloadBatchResults = async () => {
  if (!currentResult.value?.task_id) {
    ElMessage.warning("无法下载，缺少任务ID");
    return;
  }

  try {
    const response = await axios.get(
      `http://115.190.111.69:11012/tasks/${currentResult.value.task_id}/download`,
      { responseType: "blob" }
    );

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute(
      "download",
      `batch-results-${currentResult.value.task_id}.zip`
    );
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    ElMessage.success("下载成功");
  } catch (error) {
    console.error("下载失败:", error);
    ElMessage.error("下载失败，可能任务已过期或被删除");
  }
};

// 复制当前内容到剪贴板
const copyContent = () => {
  let content = "";

  if (currentResult.value) {
    if (currentResult.value.isBatch && getCurrentBatchItem.value) {
      // 如果是批量结果，复制当前查看的项
      content =
        radio.value === 3
          ? convertToXml(getCurrentBatchItem.value)
          : convertToJson(getCurrentBatchItem.value);
    } else if (!currentResult.value.isBatch) {
      // 如果是单个结果
      content =
        radio.value === 3
          ? convertToXml(currentResult.value)
          : convertToJson(currentResult.value);
    }
  }

  if (!content) {
    ElMessage.warning("没有可复制的内容");
    return;
  }

  navigator.clipboard
    .writeText(content)
    .then(() => {
      ElMessage.success("内容已复制到剪贴板");
    })
    .catch((err) => {
      console.error("复制失败:", err);
      ElMessage.error("复制失败");
    });
};

// 提取文本内容，去除HTML标签
const extractTextContent = (html) => {
  if (!html) return "";
  const tempDiv = document.createElement("div");
  tempDiv.innerHTML = html;
  return tempDiv.textContent || tempDiv.innerText || "";
};

// 将HTML内容转换为XML格式
const convertToXml = (result) => {
  if (!result || !result.content) return "<!-- 无内容 -->";

  const content = result.content;
  const title =
    content.match(/<h1>(.*?)<\/h1>/)?.[1] ||
    content.match(/<title>(.*?)<\/title>/)?.[1] ||
    "无标题";

  const textContent = extractTextContent(content);
  const paragraphs = textContent.split("\n\n").filter((p) => p.trim() !== "");

  let xml = `<?xml version="1.0" encoding="UTF-8"?>\n`;
  xml += `<article>\n`;
  xml += `  <source>${result.url || result.filename || "未知来源"}</source>\n`;
  xml += `  <date>${result.time || new Date().toLocaleString()}</date>\n`;
  xml += `  <title>${title}</title>\n`;
  xml += `  <content>\n`;

  paragraphs.forEach((paragraph, index) => {
    if (index === 0 && paragraph.includes(title)) {
      // 跳过标题段落
      return;
    }
    xml += `    <paragraph>${paragraph}</paragraph>\n`;
  });

  xml += `  </content>\n`;
  xml += `</article>`;

  return xml;
};

// 将HTML内容转换为JSON格式
const convertToJson = (result) => {
  if (!result || !result.content) return "{}";

  const content = result.content;
  const title =
    content.match(/<h1>(.*?)<\/h1>/)?.[1] ||
    content.match(/<title>(.*?)<\/title>/)?.[1] ||
    "无标题";

  const textContent = extractTextContent(content);
  const paragraphs = textContent.split("\n\n").filter((p) => p.trim() !== "");

  const jsonObj = {
    source: result.url || result.filename || "未知来源",
    date: result.time || new Date().toLocaleString(),
    title: title,
    content: paragraphs.filter((p, index) => {
      // 跳过标题段落
      return !(index === 0 && p.includes(title));
    }),
  };

  return JSON.stringify(jsonObj, null, 2);
};
</script>

<style scoped>
.results-page {
  display: flex;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.main-content {
  flex: 1;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  overflow: hidden;
  margin-left: 200px;
}

.results-header {
  margin-bottom: 2rem;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #333;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

h2 {
  font-size: 1.5rem;
  color: #666;
  font-weight: normal;
}

.batch-actions {
  display: flex;
  gap: 1rem;
}

.search-and-format {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1.5rem;
  color: #333;
}

.search-box {
  width: 300px;
  color: #333;
}

.cssbuttons-io {
  position: relative;
  font-family: inherit;
  font-weight: 500;
  font-size: 16px;
  letter-spacing: 0.05em;
  border-radius: 0.5em;
  border: none;
  background: #1fa6ffab;
  color: ghostwhite;
  overflow: hidden;
  height: 40px;
  padding: 0 12px;
  cursor: pointer;
}

.cssbuttons-io svg {
  width: 1.2em;
  height: 1.2em;
  margin-right: 0.5em;
}

.cssbuttons-io span {
  position: relative;
  z-index: 10;
  transition: color 0.4s;
  display: flex;
  align-items: center;
}

.cssbuttons-io:hover {
  background-color: #1890ff;
}

.cssbuttons-io:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.deletebutton {
  padding: 0 20px;
  height: 40px;
  line-height: 40px;
  border-radius: 0.5em;
  background-color: #ff6b6b;
  color: rgb(0, 0, 0);
  border: none;
  cursor: pointer;
  transition: all 0.3s;
}

.deletebutton:hover {
  background-color: #ff4d4f;
}

.deletebutton:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.downloadbutton {
  padding: 0 20px;
  height: 36px;
  line-height: 36px;
  border-radius: 4px;
  background-color: #52c41a;
  color: rgb(0, 0, 0);
  border: none;
  cursor: pointer;
  transition: all 0.3s;
  margin-left: 10px;
}

.downloadbutton:hover {
  background-color: #73d13d;
}

.type {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.tag {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  color: #666;
}

.deepseek {
  width: 24px;
  height: 24px;
}

.results-list {
  margin-top: 2rem;
}

.no-results {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: #999;
  background-color: white;
  border-radius: 8px;
}

.result-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.result-item {
  background-color: white;
  border-radius: 8px;
  padding: 1.2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.3s;
}

.result-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.result-item.batch-item {
  border-left: 4px solid #52c41a;
}

.result-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.result-checkbox {
  flex-shrink: 0;
}

.result-details {
  flex: 1;
}

.result-title-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.url {
  font-size: 1.2rem;
  color: #333;
  margin: 0;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.result-meta {
  display: flex;
  gap: 1rem;
}

.time,
.file-count {
  font-size: 0.9rem;
  color: #999;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

/* 批量结果对话框样式 */
.batch-controls {
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.batch-search {
  width: 300px;
}

.batch-navigation {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
}

.navigation-controls {
  display: flex;
  gap: 0.5rem;
}

.batch-file-info {
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #eee;
}

.batch-file-info h4 {
  margin: 0;
  font-size: 1rem;
  color: #333;
}

.no-batch-results {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
  color: #999;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.preview-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #333;
  margin-bottom: 1rem;
}

.result-content {
  max-height: 500px;
  overflow-y: auto;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.dialog-tabs {
  margin-bottom: 1rem;
}

.tab-buttons {
  display: flex;
  border-bottom: 1px solid #eee;
}

.tab-button {
  padding: 8px 16px;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  font-size: 16px;
  color: #666;
}

.tab-button.active {
  color: #1890ff;
  border-bottom-color: #1890ff;
  font-weight: bold;
}

.code-block {
  font-family: monospace;
  white-space: pre-wrap;
  color: #333;
  line-height: 1.5;
}

.copybutton {
  padding: 8px 20px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.copybutton:hover {
  background-color: #40a9ff;
}

.delete-content {
  padding: 1rem 0;
  color: #666;
}
</style>
