<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import AuthForm from './AuthForm.vue'
import AlertBox from '@/components/ui/AlertBox.vue'
import AuthPasswordField from './AuthPasswordField.vue'

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)
const router = useRouter()

const submitForm = async () => {
  const authStore = useAuthStore()
  isLoading.value = true
  try {
    await authStore.login(username.value, password.value)
    router.push({ name: 'home' })
  } catch (error) {
    errorMessage.value = error.response?.data.message ? error.response.data.message : error.message
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <AuthForm title="Login" @submit="submitForm">
    <AlertBox :message="errorMessage" class="mb-3 text-danger"></AlertBox>
    <div class="form-floating mb-3">
      <input
        type="text"
        class="form-control"
        id="username"
        placeholder="Username"
        v-model="username"
        required
      />
      <label for="username">Username</label>
    </div>
    <div class="form-floating mb-3">
      <AuthPasswordField
        id="password"
        label="Password"
        placeholder="Password"
        v-model="password"
      ></AuthPasswordField>
    </div>
    <button type="submit" class="btn btn-primary mb-2 w-100" :disabled="isLoading">
      <span v-if="isLoading" class="spinner-border spinner-border-sm"></span>
      {{ isLoading ? '' : 'Login' }}
    </button>
    <p class="mt-3">
      Don't have an account?
      <router-link class="text-decoration-none" to="/register">Register</router-link>
    </p>
  </AuthForm>
</template>
