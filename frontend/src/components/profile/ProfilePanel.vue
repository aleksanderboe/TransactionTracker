<script setup>
import { useAuthStore } from '@/stores/auth'
import { ref } from 'vue'

import AlertBox from '../ui/AlertBox.vue'
import ModalDialog from '../ui/ModalDialog.vue'
import router from '@/router'
import AuthPasswordField from '../auth/AuthPasswordField.vue'

const authStore = useAuthStore()
const errorMessage = ref('')
const fileInput = ref(null)
const modalOpen = ref(false)
const username = ref('')
const password = ref('')
const editMode = ref(false)

const toggleModal = (toggle) => {
  modalOpen.value = toggle
}

const submitProfilePicture = async () => {
  const file = fileInput.value.files[0]

  if (!file) {
    return
  }

  try {
    await authStore.uploadProfilePicture(file)
  } catch (error) {
    errorMessage.value = error.response?.data.message ? error.response.data.message : error.message
  }
}

const updateProfileInfo = async () => {
  try {
    await authStore.updateProfile(username.value, password.value)
    await authStore.getUser()
    toggleEdit(false)
  } catch (error) {
    errorMessage.value = error.response?.data.message ? error.response.data.message : error.message
  }
}

const deleteAccount = async () => {
  try {
    await authStore.deleteAccount()
  } catch (error) {
    errorMessage.value = error.response?.data.message ? error.response.data.message : error.message
  }

  modalOpen.value = false
  router.push({ name: 'login' })
}

const toggleEdit = (mode) => {
  editMode.value = mode
  if (!mode) {
    username.value = ''
    password.value = ''
  }
}
</script>

<template>
  <ModalDialog v-if="modalOpen" @close="toggleModal(false)">
    <template #title>Delete account</template>
    <template #body>Are you sure you wanna delete your account?</template>
    <template #footer>
      <button class="btn btn-secondary" @click="modalOpen = false">Cancel</button>
      <button class="btn btn-danger" @click="deleteAccount">Delete</button>
    </template>
  </ModalDialog>

  <div class="d-flex align-items-start justify-content-center pt-3 text-center">
    <div class="card shadow-sm" style="width: 24rem">
      <AlertBox :message="errorMessage" class="m-3"></AlertBox>

      <label for="fileUpload">
        <img
          class="card-img-top rounded-circle mx-auto mt-3 profile-picture"
          :src="authStore.profilePicture"
          alt="Profile Picture"
        />
      </label>
      <div class="card-body">
        <h5 class="card-title h3">{{ authStore.user?.username }}</h5>
        <input
          @change="submitProfilePicture"
          type="file"
          accept=".png,.jpg,.jpeg,.gif"
          ref="fileInput"
          id="fileUpload"
          class="mb-3"
          style="display: none"
        />
        <div v-if="!editMode" class="mb-3 align-items-center">
          <button class="btn " @click="toggleEdit(true)">
            <i class="bi bi-gear" style="font-size: 1.8rem;"></i>
          </button>
          <button class="btn btn-danger" @click="modalOpen = true">Delete Account</button>
        </div>
        <div v-if="editMode">
          <div class="form-floating mb-3">
            <input
              v-model="username"
              type="text"
              class="form-control"
              id="username"
              placeholder="Enter new username"
            />
            <label for="username">Enter new username</label>
          </div>
          <div class="form-floating">
            <AuthPasswordField
              id="password"
              label="Enter new password"
              placeholder="Enter new password"
              v-model="password"
            ></AuthPasswordField>
          </div>
          <button class="btn btn-primary mt-3 me-3" @click="updateProfileInfo">Save Changes</button>
          <button class="btn btn-secondary mt-3" @click="toggleEdit(false)">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-picture {
  width: 150px;
  height: 150px;
  object-fit: cover;
  cursor: pointer;
}
.profile-picture:hover {
  filter: brightness(75%);
}
</style>
