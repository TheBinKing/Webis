<template>
  <div class="app-wrapper">
    <main class="main-content">
      <router-view />
    </main>
    <div style="position: fixed; bottom: 50px; right: 45px; z-index: 999">
      <div class="tooltip-container">
        <span class="tooltip">联系我们1351482974@qq.com</span>
        <span class="text">!</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import Footer from "@/components/Footer.vue";
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  min-height: 100vh;
  color: #fff;
  box-sizing: border-box;
  overflow-x: hidden;
}

/* From Uiverse.io by Knights-kalpesh */
.tooltip-container {
  height: 50px;
  width: 80px;
  border-radius: 5px;
  background-color: #fff;
  background-image: linear-gradient(
    to left bottom,
    #f2f5f8,
    #ecf1f2,
    #e7eceb,
    #e3e7e4,
    #e1e2de
  );
  border: 1px solid white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0px 10px 10px rgba(0, 0, 0, 0.151);
  position: relative;
  transition: transform 0.3s ease;
  z-index: 999;
}

.tooltip-container::before {
  position: absolute;
  content: "";
  top: -50%;
  clip-path: polygon(50% 0, 0 100%, 100% 100%);
  border-radius: 5px;
  background-color: fff;
  background-image: linear-gradient(
    to left bottom,
    #f2f5f8,
    #e4eaec,
    #d8dfde,
    #cdd3cf,
    #c5c7c1
  );
  width: 100%;
  height: 50%;
  transform-style: preserve-3d;
  transform: perspective(1000px) rotateX(-150deg) translateY(-110%);
  transition: transform 0.3s ease;
}

.tooltip-container .text {
  color: rgb(32, 30, 30);
  font-weight: bold;
  font-size: 40px;
}

.tooltip {
  position: absolute;
  top: -20px;
  opacity: 0;
  background: linear-gradient(-90deg, rgba(0, 0, 0, 0.05) 1px, white 1px),
    linear-gradient(rgba(0, 0, 0, 0.05) 1px, white 1px),
    linear-gradient(-90deg, rgba(0, 0, 0, 0.04) 1px, white 1px),
    linear-gradient(rgba(0, 0, 0, 0.04) 1px, white 1px),
    linear-gradient(white 3px, #f2f2f2 3px, #f2f2f2 78px, white 78px),
    linear-gradient(-90deg, #aaa 1px, white 1px),
    linear-gradient(-90deg, white 3px, #f2f2f2 3px, #f2f2f2 78px, white 78px),
    linear-gradient(#aaa 1px, white 1px), #f2f2f2;
  background-size: 4px 4px, 4px 4px, 80px 80px, 80px 80px, 80px 80px, 80px 80px,
    80px 80px, 80px 80px;
  padding: 5px 10px;
  border: 1px solid rgb(206, 204, 204);

  height: 50px;
  width: 160px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition-duration: 0.2s;
  pointer-events: none;
  letter-spacing: 0.5px;
  font-size: 13px;
  font-weight: 600;
  text-shadow: 10px salmon;
  color: #323333;
}
.tooltip-container:hover {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

.tooltip-container:hover::before {
  transform: rotateY(0);
  background-image: none;
  background-color: white;
}

.tooltip-container:hover .tooltip {
  top: -55px;
  opacity: 1;
  transition-duration: 0.3s;
}

.app-wrapper {
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 0 0 0 0; /* 顶部为导航栏高度，底部为底部栏高度 */
}

* {
  box-sizing: border-box;
}

/* 全局滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(170, 171, 172, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(117, 119, 119, 0.5);
}

/* Element Plus 全局样式覆盖 */
.el-dialog {
  background: #ededed !important;
  border-radius: 12px !important;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.3) !important;
}

.el-dialog__title {
  color: #827e7e;
}

.el-dialog__header {
  border-bottom: 2px solid rgb(195, 244, 198) !important;
  padding: 20px !important;
  margin: 0 !important;
}

.el-dialog__body {
  color: #313030 !important;
  padding: 20px !important;
}

.el-dialog__footer {
  border-top: 2px solid rgb(195, 244, 198) !important;
  padding: 20px !important;
  margin: 0 !important;
}

.el-button {
  border-radius: 8px !important;
  font-weight: 500 !important;
}

.el-button--primary {
  background: linear-gradient(135deg, #4caf50, #388e3c) !important;
  border: none !important;
  color: #fff !important;
}

.el-button--primary:hover {
  background: linear-gradient(135deg, #66bb6a, #4caf50) !important;
  transform: translateY(-2px);
  box-shadow: 0 0 20px rgba(76, 175, 80, 0.3);
}

.el-button--danger {
  background: transparent !important;
  border: 1px solid rgba(255, 107, 107, 0.3) !important;
  color: #ff6b6b !important;
}

.el-button--danger:hover {
  background: rgba(255, 107, 107, 0.2) !important;
  border-color: #ff6b6b !important;
  transform: translateY(-2px);
}

.el-input__wrapper {
  background: rgba(255, 255, 255, 0.05) !important;
  box-shadow: none !important;
  border: 1px solid rgba(76, 175, 80, 0.3) !important;
}

.el-input__inner {
  color: #fff !important;
}

.el-input__wrapper.is-focus {
  box-shadow: none !important;
  border-color: #4caf50 !important;
}

.main-content-area {
  margin-left: 200px;
  width: calc(100% - 200px);
  padding: 60px 2rem 1rem;
  min-height: 100vh;
  box-sizing: border-box;
}

@media (max-width: 1200px) {
  .main-content-area {
    padding: 60px 1.5rem 1rem;
  }
}

@media (max-width: 768px) {
  .main-content-area {
    margin-left: 0;
    width: 100%;
    padding: 60px 1rem 1rem;
  }
}
</style>
