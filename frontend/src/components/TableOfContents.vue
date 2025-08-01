<template>
  <div class="toc-sidebar">
    <h3 class="toc-title">目录</h3>
    <div class="toc-content">
      <div
        v-for="(heading, index) in headings"
        :key="index"
        class="toc-item"
        :class="{ active: activeHeading === heading.id }"
        :style="{ paddingLeft: `${heading.level * 12}px` }"
        @click="scrollToHeading(heading.id)"
      >
        {{ heading.text }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";

const props = defineProps({
  content: {
    type: String,
    required: true,
  },
});

const headings = ref([]);
const activeHeading = ref("");

const extractHeadings = () => {
  const container = document.querySelector(".main-content");
  if (!container) return;

  // 只选择markdown内容中的标题，排除其他地方的标题
  const markdownContent =
    container.querySelector(".markdown-body") || container;
  const headingElements = markdownContent.querySelectorAll(
    "h1, h2, h3, h4, h5, h6"
  );

  headings.value = Array.from(headingElements).map((el) => ({
    id: el.id || `heading-${Math.random().toString(36).substr(2, 9)}`,
    text: el.textContent,
    level: parseInt(el.tagName.charAt(1)),
    offsetTop: el.offsetTop,
  }));

  // Add ids to headings if they don't have one
  headingElements.forEach((el, index) => {
    if (!el.id) {
      el.id = headings.value[index].id;
    }
  });
};

const scrollToHeading = (id) => {
  const element = document.getElementById(id);
  if (element) {
    element.scrollIntoView({ behavior: "smooth" });
    activeHeading.value = id; // 点击时立即更新 activeHeading
  }
};

const updateActiveHeading = () => {
  const scrollPosition = window.scrollY + 100; // Add offset for better UX

  for (let i = headings.value.length - 1; i >= 0; i--) {
    if (scrollPosition >= headings.value[i].offsetTop) {
      activeHeading.value = headings.value[i].id;
      break;
    }
  }
};

onMounted(() => {
  setTimeout(extractHeadings, 500); // Wait for markdown content to be rendered
  window.addEventListener("scroll", updateActiveHeading);
});

onUnmounted(() => {
  window.removeEventListener("scroll", updateActiveHeading);
});
</script>

<style scoped>
.toc-sidebar {
  width: 220px;
  position: fixed;
  left: 200px;
  top: 0;
  height: 100vh;
  background: rgba(255, 255, 255, 0.95);
  border-left: 1px solid rgba(74, 222, 128, 0.1);
  padding: 2rem 0;
  overflow-y: auto;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
}

.toc-title {
  padding: 0 1.5rem;
  margin: 0 0 1.5rem 0;
  font-size: 1.2rem;
  color: #2a2929;
  font-weight: 700;
  position: relative;
}

.toc-title::after {
  content: "";
  position: absolute;
  bottom: -8px;
  left: 1.5rem;
  width: 30px;
  height: 3px;
  background: linear-gradient(135deg, #4ade80, #3bcc65);
  border-radius: 3px;
}

.toc-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0 1rem;
}

.toc-item {
  padding: 0.8rem 1rem;
  cursor: pointer;
  font-size: 0.9rem;
  color: #606266;
  transition: all 0.3s ease;
  border-radius: 8px;
  font-weight: 500;
}

.toc-item:hover {
  background-color: rgba(74, 222, 128, 0.1);
  color: #2a2929;
  transform: translateX(5px);
}

.toc-item.active {
  color: #4ade80;
  background-color: rgba(74, 222, 128, 0.1);
  font-weight: 600;
  position: relative;
}

.toc-item.active::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 60%;
  background: linear-gradient(135deg, #4ade80, #3bcc65);
  border-radius: 3px;
}
</style>
