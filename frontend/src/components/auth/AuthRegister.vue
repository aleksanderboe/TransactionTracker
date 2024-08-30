<script setup>
import { ref } from 'vue'

import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

import AuthForm from './AuthForm.vue'
import AlertBox from '../ui/AlertBox.vue'
import InputError from '../ui/InputError.vue'

import AuthPasswordField from './AuthPasswordField.vue'

import {
  hasRange,
  hasUppercaseLetter,
  hasLowercaseLetter,
  hasDigit,
  hasSpecialCharacter
} from '@/composables/validationRules'

const username = ref('')
const usernameError = ref('')
const password = ref('')
const passwordError = ref('')
const errorMessage = ref('')
const isLoading = ref(false)
const router = useRouter()

const submitForm = async () => {
  if (!validatePassword() || !validateUsername()) {
    return
  }

  const authStore = useAuthStore()
  isLoading.value = true
  try {
    await authStore.register(username.value, password.value)
    router.push({ name: 'home' })
  } catch (error) {
    errorMessage.value = error.response?.data.message ? error.response.data.message : error.message
  } finally {
    isLoading.value = false
  }
}

const validateUsername = () => {
  if (!hasRange(username.value, 3, 30)) {
    usernameError.value = 'Username needs to be between 3 and 30 characters'
    return false
  } else {
    usernameError.value = ''
    return true
  }
}

const validatePassword = () => {
  if (!hasRange(password.value, 8, 30)) {
    passwordError.value = 'Password needs to be between 8 and 30 characteres'
    return false
  }

  if (!hasUppercaseLetter(password.value)) {
    passwordError.value = 'Password must contain at least one uppercase letter'
    return false
  }

  if (!hasLowercaseLetter(password.value)) {
    passwordError.value = 'Password must contain at least one lowercase letter'
    return false
  }
  if (!hasDigit(password.value)) {
    passwordError.value = 'Password must contain at least one digit'
    return false
  }

  if (!hasSpecialCharacter(password.value)) {
    passwordError.value = 'Password must contain at least one special character'
    return false
  }

  passwordError.value = ''
  return true
}
</script>

<template>
  <AuthForm title="Register" @submit="submitForm">
    <AlertBox :message="errorMessage" class="mb-3"></AlertBox>
    <div class="form-floating mb-3">
      <input
        type="text"
        class="form-control"
        id="username"
        placeholder="Username"
        v-model="username"
        @input="validateUsername"
        required
      />
      <label for="username">Username</label>
      <InputError :error="usernameError"></InputError>
    </div>
    <div class="form-floating mb-3">
      <AuthPasswordField
        id="password"
        label="Password"
        placeholder="Password"
        v-model="password"
        @onInputChange="validatePassword"
      ></AuthPasswordField>
      <InputError :error="passwordError"></InputError>
    </div>

    <button type="submit" class="btn btn-primary mb-2 w-100" :disabled="isLoading">
      <span v-if="isLoading" class="spinner-border spinner-border-sm"></span>
      {{ isLoading ? '' : 'Register' }}
    </button>

    <p class="mt-3">
      Already have an account?
      <router-link class="text-decoration-none" to="/login">Login</router-link>
    </p>
  </AuthForm>
</template>
