import { ref, computed, watch } from 'vue'
import { defineStore } from 'pinia'
import { jwtDecode } from 'jwt-decode'

import axios from 'axios'

const TOKEN_KEY = 'jwt'

const saveToken = (token) => {
  localStorage.setItem(TOKEN_KEY, token)
}

const removeToken = () => {
  localStorage.removeItem(TOKEN_KEY)
}

export const useAuthStore = defineStore('auth', () => {
  const getToken = () => {
    const token = localStorage.getItem(TOKEN_KEY)
    if (!token) return null

    const decoded = jwtDecode(token)
    const currentTime = Date.now() / 1000

    if (decoded.exp < currentTime) {
      removeToken()
      user.value = null
      return null
    }

    return token
  }

  const user = ref(null)

  const isAuthenticated = ref(!!getToken())

  watch(user, () => {
    isAuthenticated.value = !!getToken()
  })

  const profilePicture = computed(() =>
    user.value?.profile_picture
      ? `${import.meta.env.VITE_APP_API_URL}/auth/uploads/${user.value?.profile_picture}`
      : `https://fakeimg.pl/500x500?text=${user.value?.username}`
  )

  const register = async (username, password) => {
    const response = await axios.post('/auth/register', { username, password })
    saveToken(response.data.access_token)
    await getUser()
  }

  const login = async (username, password) => {
    const response = await axios.post('/auth/login', { username, password })
    saveToken(response.data.access_token)
    await getUser()
  }

  const getUser = async () => {
    const token = getToken()
    if (!token) {
      return
    }

    const response = await axios.get('/auth/user', {
      headers: { Authorization: `Bearer ${token}` }
    })
    user.value = response.data
  }

  const logout = async () => {
    const token = getToken()
    await axios.post('/auth/logout', {}, { headers: { Authorization: `Bearer ${token}` } })
    user.value = null
    removeToken()
  }

  const updateProfile = async (username, password) => {
    const token = getToken()
    await axios.put(
      '/auth/update-profile',
      { username: username, password: password },
      { headers: { Authorization: `Bearer ${token}` } }
    )
  }

  const deleteAccount = async () => {
    const token = getToken()
    await axios.post('/auth/delete-account', {}, { headers: { Authorization: `Bearer ${token}` } })
    user.value = null
    removeToken()
  }

  const uploadProfilePicture = async (file) => {
    const token = getToken()
    const formData = new FormData()
    formData.append('file', file)
    await axios.post('/auth/upload-profile-picture', formData, {
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'multipart/form-data' }
    })
    await getUser()
  }

  return {
    user,
    isAuthenticated,
    register,
    login,
    getUser,
    logout,
    uploadProfilePicture,
    updateProfile,
    deleteAccount,
    profilePicture
  }
})
