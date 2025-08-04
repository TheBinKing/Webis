import { ref } from 'vue'

export const currentUser = ref(null)

export const updateCurrentUser = (user) => {
    currentUser.value = user
} 