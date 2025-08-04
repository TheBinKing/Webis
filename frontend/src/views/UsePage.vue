<template>
  <div class="use-page">
    <Sidebar />
    <div class="main-content">
      <div class="use-header">
        <h1>CLEAN</h1>
        <h2>清洗网页并生成可供LLM使用的数据格式</h2>
      </div>
      <!-- From Uiverse.io by Yaya12085 -->
      <div class="radio-inputs">
        <label class="radio">
          <input
            type="radio"
            name="radio"
            value="single"
            v-model="selectedRadio"
          />
          <span class="name">简单爬取</span>
        </label>
        <label class="radio">
          <input
            type="radio"
            name="radio"
            checked
            value="single"
            v-model="selectedRadio"
          />
          <span class="name">单页面清洗</span>
        </label>

        <label class="radio">
          <input
            type="radio"
            name="radio"
            value="multiple"
            v-model="selectedRadio"
          />
          <span class="name">多页面清洗</span>
        </label>
      </div>
      <div class="function">
        <Single v-show="selectedRadio == 'single'"></Single>
        <Multiple v-show="selectedRadio == 'multiple'"></Multiple>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Sidebar from "@/components/Sidebar.vue";
import { HomeFilled, Brush, Document } from "@element-plus/icons-vue";
import Single from "@/components/Single.vue";
import Multiple from "@/components/Multiple.vue";

const selectedRadio = ref("single");
</script>

<style scoped>
.use-page {
  display: flex;
  min-height: 100vh;
  background: #ffffff;
}

.main-content {
  flex: 1;
  padding: 2rem;
  padding-bottom: 0px;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  overflow: hidden;
  margin-left: 200px;
}

.use-header h1 {
  color: hsl(0, 0%, 11%);
  text-shadow: 0 0 20px rgba(84, 201, 111, 0.5);
  font-size: 2.2rem;
  font-weight: 600;
}
.use-header h2 {
  margin-top: 2.5rem;
  color: hsl(200, 1%, 50%);
  font-size: 1.3rem;
  font-weight: 500;
}

.function {
  padding: 1rem;
  background-color: rgba(224, 221, 221, 0.295);
  border-radius: 0.5rem;
}

.placeholder {
  color: rgba(255, 255, 255, 0.5);
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

/*单选框样式*/
/* From Uiverse.io by Yaya12085 */
.radio-inputs {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  border-radius: 0.5rem;
  background-color: #eee;
  box-sizing: border-box;
  box-shadow: 0 0 0px 1px rgba(0, 0, 0, 0.06);
  padding: 0.25rem;
  width: 400px;
  font-size: 16px;
}

.radio-inputs .radio {
  flex: 1 1 auto;
  text-align: center;
}

.radio-inputs .radio input {
  display: none;
}

.radio-inputs .radio .name {
  display: flex;
  cursor: pointer;
  align-items: center;
  justify-content: center;
  border-radius: 0.5rem;
  border: none;
  padding: 0.5rem 0;
  color: rgba(51, 65, 85, 1);
  transition: all 0.15s ease-in-out;
}

.radio-inputs .radio input:checked + .name {
  background-color: #fff;
  font-weight: 600;
}
</style>
