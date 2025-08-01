<script setup>
// 技术栈数据
const techStacks = [
  {
    name: "MAS",
    description: "MAS三层级语义分析显著降低密钥检测误报率",
    icon: "🌟",
  },
  { name: "LLM", description: "强化学习增强MAS稳定性和适应性", icon: "🛣️" },
  {
    name: "MCP",
    description: "MCP实现读取-检测-屏蔽功能一体化",
    icon: "🍍",
  },
];
</script>

<template>
  <main class="home">
    <div class="container">
      <div class="hero-section">
        <div class="hero-content">
          <div class="tag">
            <img src="@/assets/Deepseek.png" class="deepseek" />
            采用MAS三层级语义分析
          </div>
          <h1 class="title1">基于强化学习多智能体系统</h1>
          <h1 class="title">一键提取密钥</h1>
          <h2 class="subtitle">高效文件秘密保护框架</h2>
          <button class="cta-button">点击立即体验</button>
        </div>
        <div class="hero-image">
          <img
            src="@/assets/2.png"
            alt="网页去噪工具界面"
            class="hero-screenshot"
          />
        </div>
      </div>
      <div class="preview">
        <h1 class="preview-title">创新性概览</h1>
        <p class="subtitle">基于强化学习多智能体系统的秘密保护框架</p>

        <div class="tabs">
          <div class="tab active">主要创新点</div>
        </div>

        <div class="tech-stack-grid">
          <div
            v-for="(tech, index) in techStacks"
            :key="index"
            class="tech-card"
          >
            <div class="tech-icon">{{ tech.icon }}</div>
            <h3>{{ tech.name }}</h3>
            <p>{{ tech.description }}</p>
          </div>
        </div>

        <div class="info-text">
          <p>探索我们使用的先进技术栈</p>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.home {
  padding: 0;
  background-color: #fff;
  width: 100%;
}

.preview {
  padding: 3rem 0;
  width: 100%;
}

.preview-title {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
}

.subtitle {
  color: #666;
  margin-bottom: 2.5rem;
  font-size: 1.1rem;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #eee;
  margin-bottom: 2rem;
}

.tab {
  padding: 0.5rem 1rem;
  margin-right: 1rem;
  font-weight: 500;
  color: #555;
  cursor: pointer;
  border-bottom: 2px solid transparent;
}

.tab.active {
  color: #ff6b35;
  border-bottom: 2px solid #ff6b35;
}

.tech-stack-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 4rem;
  margin-bottom: 3rem;
}

.tech-card {
  padding: 2rem;
  border-radius: 8px;
  background-color: #f9f9f9;
  transition: transform 0.3s ease;
}

.tech-card:hover {
  transform: translateY(-5px);
}

.tech-icon {
  font-size: 3rem;
  margin-bottom: 1.5rem;
}

h3 {
  margin-bottom: 0.8rem;
  color: #333;
  font-weight: 600;
  font-size: 1.2rem;
}

p {
  color: #666;
  font-size: 1rem;
  line-height: 1.6;
}

.info-text {
  margin-top: 3rem;
  text-align: center;
  color: #666;
  font-style: italic;
  font-size: 1rem;
}

@media (max-width: 768px) {
  .preview {
    padding: 2rem 0;
  }

  .tech-stack-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .tech-card {
    padding: 1.5rem;
  }
}
.hero-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6rem 8rem;
  min-height: 600px;
  position: relative;
  overflow: hidden;
  margin-top: 4vh;
  padding-top: calc(6rem + 70px);
  background: #f3f5f4;
  border-radius: 20px;
}

.hero-section::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.hero-content {
  flex: 1;
  max-width: 600px;
  position: relative;
  z-index: 1;
  padding-right: 2rem;
}

.subtitle {
  color: hsl(200, 1%, 50%);
  font-size: 1.5rem;
  font-weight: 500;
  margin-top: 2rem;
  opacity: 0.9;
  letter-spacing: 1px;
  text-shadow: 0 0 20px rgba(76, 201, 240, 0.3);
}

.title {
  color: hsl(0, 0%, 11%);
  font-size: 3.8rem;
  font-weight: 700;
  line-height: 1.2;
  text-shadow: 0 0 20px rgba(249, 158, 78, 0.3);
  letter-spacing: -1px;
}
.title1 {
  color: hsl(34, 79%, 55%);
  font-size: 3rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 1rem;
  text-shadow: 0 0 20px rgba(216, 133, 17, 0.3);
  letter-spacing: -1px;
}
.tag {
  background-color: #fff;
  box-shadow: 0 0 10px rgba(94, 95, 95, 0.3);
  border-radius: 20px;
  color: #373838;
  display: inline-block;
  font-size: 0.8rem;
  padding: 0.5rem 0.8rem;
  padding-left: 30px;
  position: relative;
  font-weight: 700;
  margin-bottom: 20px;
}
.deepseek {
  width: 20px;
  position: absolute;
  left: 4px;
}
.cta-button {
  background: #373838;
  color: #fff;
  border: none;
  padding: 1.2rem 2.8rem;
  font-size: 1.2rem;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 0 30px rgba(76, 201, 240, 0.3);
  margin-top: 10px;
}

.cta-button:hover {
  background: linear-gradient(135deg, #f1cf9f, #ecb43b);
  transform: translateY(-2px);
  box-shadow: 0 0 40px rgba(231, 150, 28, 0.5);
}

.cta-button:active {
  transform: translateY(1px);
}

.hero-image {
  margin-left: 2rem;
}

.hero-screenshot {
  width: 650px;
  height: 350px;
  display: block;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(224, 192, 116, 0.3);
  transition: transform 0.3s ease;
}

.hero-screenshot:hover {
  transform: scale(1.02);
}

@media (max-width: 1280px) {
  .hero-section {
    padding: 5rem 4rem;
  }

  .title {
    font-size: 3.2rem;
  }
}

@media (max-width: 1024px) {
  .hero-section {
    padding: 4rem 2rem;
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 3rem 1.5rem;
  }
}
</style> 