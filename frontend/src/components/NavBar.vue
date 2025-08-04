<template>
  <nav class="navbar">
    <router-link to="/" class="logo-container">
      <div class="logo-wrapper">
        <img
          src="@/assets/logo2.svg"
          alt="Web Denoising Tool Logo"
          class="logo"
        />
        <div class="logo-glow"></div>
      </div>
      <div class="brand-text">
        <span class="logo-text">Webis</span>
      </div>
    </router-link>
  </nav>
</template>

<script setup>
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2.5rem;
  z-index: 1000;
  border-bottom: 1px solid rgba(74, 222, 128, 0.1);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
}

.logo-container {
  display: flex;
  align-items: center;
  text-decoration: none;
  gap: 1.2rem;
  padding: 0.8rem;
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.logo-wrapper {
  position: relative;
  width: 40px;
  height: 40px;
  background: rgba(74, 222, 128, 0.1);
  border-radius: 12px;
  padding: 8px;
  transition: all 0.3s ease;
}

.logo {
  height: 100%;
  width: 100%;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  z-index: 1;
}

.logo-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  background: radial-gradient(
    circle,
    rgba(74, 222, 128, 0.2) 0%,
    rgba(74, 222, 128, 0) 70%
  );
  opacity: 0;
  transition: all 0.3s ease;
  border-radius: 12px;
}

.logo-container:hover .logo-wrapper {
  background: rgba(74, 222, 128, 0.2);
  transform: translateY(-2px);
}

.logo-container:hover .logo {
  transform: scale(1.1) rotate(5deg);
}

.logo-container:hover .logo-glow {
  opacity: 1;
  transform: translate(-50%, -50%) scale(1.5);
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.logo-text {
  font-size: 1.5rem;
  color: #2a2929;
  font-weight: 700;
  text-shadow: 0 0 10px rgba(74, 222, 128, 0.2);
  transition: all 0.3s ease;
  line-height: 1.2;
  letter-spacing: -0.5px;
}

.logo-container:hover .logo-text {
  text-shadow: 0 0 20px rgba(74, 222, 128, 0.3);
  color: #4ade80;
}

.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.start-button1 {
  background: linear-gradient(135deg, #4ade80, #3bcc65);
  border: none;
  border-radius: 12px;
  padding: 0.8rem 1.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  color: white;
  box-shadow: 0 4px 15px rgba(74, 222, 128, 0.3);
}

.start-button1:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(74, 222, 128, 0.4);
}

.auth-button {
  background-color: transparent;
  border: 2px solid #4ade80;
  border-radius: 12px;
  padding: 0.8rem 1.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  color: #4ade80;
  cursor: pointer;
}

.auth-button:hover {
  background-color: #4ade80;
  color: white;
  transform: translateY(-2px);
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(135deg, #4ade80, #3bcc65);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(74, 222, 128, 0.2);
}

.user-avatar:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 6px 20px rgba(74, 222, 128, 0.3);
}

.admin-link {
  color: #4ade80;
  text-decoration: none;
  font-weight: 600;
  padding: 0.8rem 1.5rem;
  border-radius: 12px;
  background-color: rgba(74, 222, 128, 0.1);
  transition: all 0.3s ease;
}

.admin-link:hover {
  background-color: rgba(74, 222, 128, 0.2);
  transform: translateY(-2px);
}
</style>
