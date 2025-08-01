import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0,
    name: 'Counter',
    isAdmin: true
  }),
  getters: {
    doubleCount: (state) => state.count * 2
  },
  actions: {
    increment() {
      this.count++
    },
    decrement() {
      this.count--
    },
    reset() {
      this.count = 0
    },
    setAdmin(value) {
      this.isAdmin = value
    }
  },
  persist: {
    // 持久化配置
    key: 'counter-store', // 存储的键名
    storage: localStorage, // 使用 localStorage
    paths: ['count', 'isAdmin'], // 持久化 count 和 isAdmin 字段
  }
})
