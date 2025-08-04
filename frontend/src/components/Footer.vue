<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-section">
        <p class="copyright">
          {{ currentYear }} Web Denoising Tool. All Rights Reserved.
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref, onMounted } from "vue";

const currentYear = ref(new Date().getFullYear());
</script>

<style scoped>
.footer {
  background: rgba(0, 0, 0, 0.95);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(74, 222, 128, 0.1);
  padding: 0.5rem 0;
  z-index: 1000;
  height: 4vh;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.footer-section {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.copyright {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.85rem;
  margin: 0;
}

@media (max-width: 768px) {
  .footer-content {
    text-align: center;
  }
}
</style>
