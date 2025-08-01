import { createRouter, createWebHashHistory } from "vue-router";

// 定义路由
const routes = [
  {
    path: "/",
    name: "Home",
    component: () => import("../views/Home.vue"),
    meta: { requiresAuth: true },
  },

  {
    path: "/usepage",
    name: "UsePage",
    component: () => import("../views/UsePage.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/results",
    name: "Results",
    component: () => import("../views/Results.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/docs",
    name: "Docs",
    component: () => import("../views/Docs.vue"),
  },
  // 处理不匹配的路由
  {
    path: "/:pathMatch(.*)*",
    redirect: "/",
  },
];

// 创建路由实例
const router = createRouter({
  history: createWebHashHistory(),
  routes,
});



export default router;
