<template>
  <div class="docs-page">
    <sidebar></sidebar>
    <div class="main-content">
      <div class="markdown-body"><Md></Md></div>
    </div>
    <table-of-contents :content="markdownContent"></table-of-contents>
    <!-- From Uiverse.io by boryanakrasteva -->
    <div class="search">
      <div class="input-container">
        <input type="text" name="text" class="input" placeholder="search..." />
        <span class="icon">
          <svg
            width="19px"
            height="19px"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
            <g
              id="SVGRepo_tracerCarrier"
              stroke-linecap="round"
              stroke-linejoin="round"
            ></g>
            <g id="SVGRepo_iconCarrier">
              <path
                opacity="1"
                d="M14 5H20"
                stroke="#000"
                stroke-width="1.5"
                stroke-linecap="round"
                stroke-linejoin="round"
              ></path>
              <path
                opacity="1"
                d="M14 8H17"
                stroke="#000"
                stroke-width="1.5"
                stroke-linecap="round"
                stroke-linejoin="round"
              ></path>
              <path
                d="M21 11.5C21 16.75 16.75 21 11.5 21C6.25 21 2 16.75 2 11.5C2 6.25 6.25 2 11.5 2"
                stroke="#000"
                stroke-width="2.5"
                stroke-linecap="round"
                stroke-linejoin="round"
              ></path>
              <path
                opacity="1"
                d="M22 22L20 20"
                stroke="#000"
                stroke-width="3.5"
                stroke-linecap="round"
                stroke-linejoin="round"
              ></path>
            </g>
          </svg>
        </span>
      </div>
    </div>
  </div>
</template>
<script setup>
import Sidebar from "@/components/Sidebar.vue";
import TableOfContents from "@/components/TableOfContents.vue";
import Md from "./WebFLow_server_description.md";
import { ref, onMounted } from "vue";

const markdownContent = ref("");

onMounted(() => {
  markdownContent.value = document.querySelector(".markdown-body").innerHTML;
});
</script>
<style scoped>
.docs-page {
  display: flex;
  min-height: 100vh;
  background: #ffffff;
}

.main-content {
  flex: 1;
  padding: 2rem;
  overflow: auto;
  margin-left: 200px;
  margin-right: 220px;
  color: black;
}

/* Add styles for markdown headings */
:deep(h1),
:deep(h2),
:deep(h3),
:deep(h4),
:deep(h5),
:deep(h6) {
  scroll-margin-top: 2rem;
}

.markdown-body {
  width: 100%;
  max-width: 900px;
  margin-left: 120px;
}

/* From Uiverse.io by boryanakrasteva */
.search {
  position: fixed;
  top: 20px;
  right: 20px;
}
.input-container {
  width: 220px;
  position: relative;
}

.icon {
  position: absolute;
  right: 10px;
  top: calc(50% + 5px);
  transform: translateY(calc(-50% - 5px));
}

.input {
  width: 100%;
  height: 40px;
  padding: 10px;
  transition: 0.2s linear;
  border: 2.5px solid rgb(100, 99, 99);
  border-radius: 15px;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.input:focus {
  outline: none;
  border: 0.5px solid rgb(77, 199, 39);
  box-shadow: -5px -5px 0px rgb(43, 211, 1);
}

.input-container:hover > .icon {
  animation: anim 1s linear infinite;
}

@keyframes anim {
  0%,
  100% {
    transform: translateY(calc(-50% - 5px)) scale(1);
  }

  50% {
    transform: translateY(calc(-50% - 5px)) scale(1.1);
  }
}
</style>
