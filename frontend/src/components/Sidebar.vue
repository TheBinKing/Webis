<template>
  <div class="sidebar">
    <div class="logo">
      <img src="@/assets/logo2.svg" alt="Logo" />
      <p>Webis</p>
    </div>
    <nav class="nav-menu">
      <router-link to="/" class="nav-item">
        <el-icon><HomeFilled /></el-icon>
        <span>HOME</span>
      </router-link>
      <router-link to="/usepage" class="nav-item">
        <el-icon><Brush /></el-icon>
        <span>CLEAN</span>
      </router-link>
      <router-link to="/results" class="nav-item">
        <el-icon><Document /></el-icon>
        <span>RESULTS</span>
      </router-link>
      <router-link to="/docs" class="nav-item">
        <el-icon><Document /></el-icon>
        <span>DOCS</span>
      </router-link>
    </nav>
  </div>
</template>

<script setup>
import { HomeFilled, Brush, Document } from "@element-plus/icons-vue";
</script>

<style scoped>
.sidebar {
  width: 200px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 2rem 1.5rem;
  border-right: 1px solid rgba(74, 222, 128, 0.1);
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100%;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
}

.logo {
  text-align: center;
  margin-bottom: 2rem;
  padding: 1rem;
  background: rgba(74, 222, 128, 0.1);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.logo:hover {
  transform: translateY(-2px);
  background: rgba(74, 222, 128, 0.15);
}

.logo img {
  width: 50px;
  height: auto;
  margin-bottom: 0.5rem;
}

.logo p {
  color: #2a2929;
  font-weight: 700;
  font-size: 1.4rem;
  text-shadow: 0 0 10px rgba(74, 222, 128, 0.2);
  letter-spacing: -0.5px;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  color: rgba(0, 0, 0, 0.8);
  text-decoration: none;
  border-radius: 12px;
  transition: all 0.3s ease;
  font-size: 1rem;
  font-weight: 500;
}

.nav-item:hover {
  background-color: rgba(74, 222, 128, 0.1);
  transform: translateX(5px);
}

.nav-item.router-link-active {
  background: linear-gradient(135deg, #4ade80, #3bcc65);
  color: white;
  box-shadow: 0 4px 15px rgba(74, 222, 128, 0.3);
}

.nav-item .el-icon {
  font-size: 1.2rem;
  transition: all 0.3s ease;
}

.nav-item:hover .el-icon {
  transform: scale(1.1);
}
</style>
