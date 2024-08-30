<script setup>
import ModalDialog from '../ui/ModalDialog.vue'
import InputError from '../ui/InputError.vue'
import AlertBox from '../ui/AlertBox.vue'
import { useCategoryStore } from '@/stores/categories'
import { useCategoryFunctions } from '@/composables/transactionCategoryModal'

const categoryStore = useCategoryStore()
const { 
  nameError,
  errorMessage,
  isLoading,
  showCategories,
  showDeleteConfirm,
  name,
  color,
  selectedCategories,
  currentPage,
  searchQuery,
  validateName,
  handleClose,
  handleSubmit,
  handleShowCategories,
  confirmDeleteCategories,
  deleteSelectedCategories,
  handleCancelDelete,
  paginatedCategories,
  totalPages,
  nextPage,
  prevPage,
  handleSearch
} = useCategoryFunctions()

const emit = defineEmits(['close'])
</script>

<template>
  <form @submit.prevent="handleSubmit(emit)">
    <ModalDialog @close="() => handleClose(emit)">
      <template #title> Add Category </template>
      <template #body>
        <AlertBox :message="errorMessage" class="mb-3"></AlertBox>
        <div class="form-floating mb-3">
          <input
            type="text"
            class="form-control"
            id="name"
            name="name"
            placeholder="name"
            v-model="name"
            maxlength="20"
            @input="validateName"
          />
          <label for="name">Name</label>
          <InputError :error="nameError"></InputError>
        </div>
        <label for="color">Choose a color</label>
        <input
          class="w-100 border-0"
          type="color"
          id="color"
          name="color"
          placeholder="color"
          v-model="color"
        />
        <p>Preview</p>
        <span class="badge fs-5" :style="{ backgroundColor: color }">{{ name || 'Preview' }}</span>
        <hr/>
        <button type="button" @click="handleShowCategories" class="btn btn-dark w-100" :disabled="isLoading">
          <span v-if="isLoading" class="spinner-border spinner-border-sm"></span>
          {{ isLoading ? '' : 'Show Categories' }}
        </button>
        <div v-if="showCategories" class="mt-3">
          <div v-if="categoryStore.categories.length > 0">
            <h3>Categories</h3>
            <input 
              type="text" 
              class="form-control mb-3" 
              placeholder="Search categories" 
              v-model="searchQuery"
              @input="handleSearch"
            />
            <ul v-if="paginatedCategories.length > 0" class="list-group">
              <li v-for="category in paginatedCategories" :key="category.id" class="list-group-item d-flex justify-content-between align-items-center">
                <span>
                  <span class="badge me-2" :style="{ backgroundColor: category.color }">&nbsp;</span>
                  {{ category.name }}
                </span>
                <input type="checkbox" :value="category.id" v-model="selectedCategories" class="form-check-input">
              </li>
            </ul>
            <p v-else>No categories found</p>
            <div v-if="totalPages > 1" class="d-flex justify-content-between align-items-center mt-3">
              <button type="button" @click="prevPage" class="btn btn-secondary" :disabled="currentPage === 1">Previous</button>
              <span>Page {{ currentPage }} of {{ totalPages }}</span>
              <button type="button" @click="nextPage" class="btn btn-secondary" :disabled="currentPage === totalPages">Next</button>
            </div>
            <button v-if="categoryStore.categories.length > 0" type="button" @click="confirmDeleteCategories" class="btn btn-danger mt-3">Delete Selected</button>
          </div>
          <p v-else>No categories available</p>
        </div>
      </template>
      <template #footer>
        <button type="submit" class="btn btn-dark w-100" :disabled="isLoading">
          <span v-if="isLoading" class="spinner-border spinner-border-sm"></span>
          {{ isLoading ? '' : 'Add Category' }}
        </button>
      </template>
    </ModalDialog>

    <ModalDialog v-if="showDeleteConfirm" @close="handleCancelDelete">
      <template #title>Confirm Deletion</template>
      <template #body>
        <p>Are you sure you want to delete the selected categories?</p>
      </template>
      <template #footer>
        <button type="button" class="btn btn-secondary" @click="handleCancelDelete">Cancel</button>
        <button type="button" class="btn btn-danger" @click="deleteSelectedCategories(emit)">Delete</button>
      </template>
    </ModalDialog>
  </form>
</template>

<style scoped></style>
