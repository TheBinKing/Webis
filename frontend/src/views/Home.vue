<template>
  <NavBar />
  <div class="home main-content-area">
    <div class="hero-section">
      <div class="hero-content">
        <div class="tag">
          <img src="@/assets/Deepseek.png" class="deepseek" />基于DeepSeek-R1
          1.5B大模型
        </div>
        <h1 class="title">一键净化网页</h1>
        <h1 class="title1">为LLM提供高效数据</h1>
        <h2 class="subtitle">高效数据清洗流水线框架</h2>
        <button class="cta-button" @click="$router.push('/usepage')">
          点击立即体验
        </button>
      </div>
      <div class="hero-image">
        <img
          src="@/assets/weidu.png"
          alt="网页去噪工具界面"
          class="hero-screenshot"
        />
      </div>
    </div>
    <div class="content-container">
      <section class="section">
        <h2 class="section-title" data-aos="fade-right">解决痛点</h2>
        <div class="pain-points">
          <div class="pain-point" data-aos="fade-up" data-aos-delay="100">
            <div class="point-content">
              <h3>广告干扰</h3>
              <p>智能识别和移除各类广告内容，还原纯净阅读体验</p>
            </div>
          </div>
          <div class="pain-point" data-aos="fade-up" data-aos-delay="200">
            <div class="point-content">
              <h3>内容混乱</h3>
              <p>自动整理页面结构，突出重点内容展示</p>
            </div>
          </div>
          <div class="pain-point" data-aos="fade-up" data-aos-delay="300">
            <div class="point-content">
              <h3>三层处理</h3>
              <p>三层处理，领先市场同类型净化产品</p>
            </div>
          </div>
        </div>
      </section>
      <section class="section steps-section">
        <div class="steps-container">
          <h2 class="steps-title">使用步骤</h2>
          <div class="timeline">
            <div class="timeline-item" data-aos="fade-up" data-aos-delay="100">
              <div class="timeline-number">1</div>
              <div class="timeline-content">
                <h3>输入网页地址</h3>
                <p>输入您想要处理的网页URL地址</p>
              </div>
            </div>
            <div class="timeline-item" data-aos="fade-up" data-aos-delay="200">
              <div class="timeline-number">2</div>
              <div class="timeline-content">
                <h3>训练提取器</h3>
                <p>系统智能学习网页结构特征</p>
              </div>
            </div>
            <div class="timeline-item" data-aos="fade-up" data-aos-delay="300">
              <div class="timeline-number">3</div>
              <div class="timeline-content">
                <h3>提取数据</h3>
                <p>自动提取并整理所需内容</p>
              </div>
            </div>
          </div>
        </div>
      </section>
      <section class="section">
        <h2 class="section-title" data-aos="fade-right">开始使用</h2>
        <div class="start-section">
          <router-link to="/usepage" class="start-button"
            >Start Using</router-link
          >
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from "vue";
import gsap from "gsap";
import NavBar from "@/components/NavBar.vue";

// 添加鼠标移动视差效果
let mouseX = 0;
let mouseY = 0;

const handleMouseMove = (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;

  const cards = document.querySelectorAll(".tech-card");
  cards.forEach((card) => {
    const rect = card.getBoundingClientRect();
    const cardX = rect.left + rect.width / 2;
    const cardY = rect.top + rect.height / 2;

    const moveX = (mouseX - cardX) * 0.01;
    const moveY = (mouseY - cardY) * 0.01;

    gsap.to(card, {
      x: moveX,
      y: moveY,
      duration: 0.3,
      ease: "power2.out",
    });
  });
};

onMounted(() => {
  window.addEventListener("mousemove", handleMouseMove);
});

onUnmounted(() => {
  window.removeEventListener("mousemove", handleMouseMove);
});
</script>

<style scoped>
.home {
  min-height: 100vh;
  left: -5%;
  padding: 2rem;
  background: #fff;
  position: relative;
  overflow: hidden;
}

.main-content {
  margin-left: 200px;
  padding: 0 2rem;
  width: calc(100% - 200px);
}

.hero-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8rem 8rem;
  min-height: 600px;
  position: relative;
  overflow: hidden;
  margin-top: 6vh;
  padding-top: calc(6rem + 70px);
  margin-bottom: 14vh;
  background: #f8f9f8;
  border-radius: 24px;
  box-shadow: 0 0 30px rgba(74, 222, 128, 0.1);
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
  padding-right: 4rem;
}

.subtitle {
  color: hsl(200, 1%, 50%);
  font-size: 1.5rem;
  font-weight: 500;
  margin-top: 2rem;
  opacity: 0.9;
  letter-spacing: 1px;
  text-shadow: 0 0 20px rgba(74, 222, 128, 0.3);
}

.title {
  color: hsl(0, 0%, 11%);
  font-size: 3.8rem;
  font-weight: 700;
  line-height: 1.2;
  text-shadow: 0 0 20px rgba(76, 201, 240, 0.3);
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
  box-shadow: 0 0 30px rgba(74, 222, 128, 0.3);
  margin-top: 20px;
}

.cta-button:hover {
  background: linear-gradient(135deg, #4ade80, #3bcc65);
  transform: translateY(-2px);
  box-shadow: 0 0 40px rgba(74, 222, 128, 0.5);
}

.cta-button:active {
  transform: translateY(1px);
}

.hero-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 55%;
  position: relative;
  z-index: 1;
  perspective: 2000px;
  padding-left: 2rem;
}

.hero-screenshot {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(74, 222, 128, 0.3);
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

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
}

.section {
  margin-bottom: 6rem;
  position: relative;
}

.section-title {
  font-size: 2.5rem;
  margin-bottom: 3rem;
  color: #4ade80;
  text-shadow: 0 0 15px rgba(74, 222, 128, 0.4);
}

.steps-section {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 4rem 2rem;
}

.steps-container {
  display: flex;
  align-items: center;
  gap: 6rem;
  max-width: 1200px;
  margin: 0 auto;
}

.steps-title {
  font-size: 2.5rem;
  color: #292828;
  margin: 0;
  padding-right: 200px;
  white-space: nowrap;
  min-width: 120px;
  text-shadow: 0 0 20px rgba(74, 222, 128, 0.3);
}

.timeline {
  flex-grow: 1;
  position: relative;
  padding: 2rem 0;
}

.timeline::before {
  content: "";
  position: absolute;
  left: 25px;
  width: 2px;
  height: 100%;
  background: linear-gradient(
    to bottom,
    rgba(74, 222, 128, 0) 0%,
    rgba(74, 222, 128, 0.6) 10%,
    rgba(74, 222, 128, 0.6) 90%,
    rgba(74, 222, 128, 0) 100%
  );
  top: 0;
}

.timeline-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 4rem;
  position: relative;
  padding-left: 60px;
}

.timeline-number {
  width: 50px;
  height: 50px;
  background: #4ade80;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: #fff;
  font-weight: bold;
  position: absolute;
  left: 0;
  top: 0;
  z-index: 2;
  box-shadow: 0 0 20px rgba(74, 222, 128, 0.3);
}

.timeline-content {
  padding: 0.5rem 0;
  flex-grow: 1;
  transition: all 0.3s ease;
}

.timeline-content h3 {
  font-size: 1.5rem;
  color: #4ade80;
  margin-bottom: 0.5rem;
}

.timeline-content p {
  color: rgba(57, 55, 55, 0.8);
  font-size: 1.1rem;
  line-height: 1.6;
}

.timeline-item:hover .timeline-number {
  transform: scale(1.1);
  background: #7de79f;
  box-shadow: 0 0 30px rgba(74, 222, 128, 0.5);
}

.pain-points {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin: 0 auto;
  max-width: 1200px;
}

.pain-point {
  height: 300px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 2rem;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(74, 222, 128, 0.2);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  transform-style: preserve-3d;
  box-shadow: 0 0 20px rgba(74, 222, 128, 0.1);
}

.point-content {
  padding: 2rem;
  position: relative;
  z-index: 1;
  background: linear-gradient(135deg, rgba(74, 222, 128, 0.1), transparent);
  border: 1px solid rgba(74, 222, 128, 0.2);
  border-radius: 15px;
  transition: all 0.3s ease;
}

.point-content:hover {
  transform: translateY(-5px);
  border-color: #4ade80;
  box-shadow: 0 0 20px rgba(74, 222, 128, 0.2);
}

h3 {
  color: #4ade80;
  margin-bottom: 1rem;
  font-size: 1.5rem;
  text-shadow: 0 0 10px rgba(74, 222, 128, 0.3);
}

p {
  color: #454545;
  line-height: 1.6;
  opacity: 0.8;
  font-weight: 800;
}

.start-section {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 3rem 0;
}

.start-button {
  font-size: 1.8rem;
  padding: 1.2rem 3rem;
  border-radius: 50px;
  background: linear-gradient(135deg, #4ade80, #3bcc65);
  color: #fff;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  text-transform: none;
  position: relative;
  overflow: hidden;
  box-shadow: 0 0 30px rgba(74, 222, 128, 0.3);
  text-decoration: none;
}

.start-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 40px rgba(74, 222, 128, 0.5);
  background: linear-gradient(135deg, #7de79f, #4ade80);
}

.start-button:active {
  transform: translateY(1px);
}

.start-button::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    120deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: 0.5s;
}

.start-button:hover::before {
  left: 100%;
}

@media (max-width: 768px) {
  .steps-container {
    flex-direction: column;
    gap: 2rem;
    align-items: center;
  }

  .steps-title {
    text-align: center;
  }

  .timeline {
    width: 100%;
  }
}
.title1 {
  color: hsl(142, 76%, 58%);
  font-size: 3.8rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 1rem;
  text-shadow: 0 0 20px rgba(74, 222, 128, 0.3);
  letter-spacing: -1px;
}
</style>
