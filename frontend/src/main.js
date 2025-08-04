import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";

// 创建应用实例
const app = createApp(App);
const pinia = createPinia();

// 注册Element Plus
app.use(ElementPlus, { size: "default", zIndex: 2000 });

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

app.use(pinia);

app.use(router);

// 挂载应用
app.mount("#app");

// 启动应用
initApp();

