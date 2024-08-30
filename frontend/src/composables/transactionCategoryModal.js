import { ref, computed } from 'vue'
import { useCategoryStore } from '@/stores/categories'
import { hasRange } from '@/composables/validationRules'

export const useCategoryFunctions = () => {
  const nameError = ref('')
  const errorMessage = ref('')
  const isLoading = ref(false)
  const showCategories = ref(false)
  const showDeleteConfirm = ref(false)
  const name = ref('')
  const color = ref('#16813D')
  const selectedCategories = ref([]); 
  const currentPage = ref(1)
  const itemsPerPage = 3
  const searchQuery = ref('')

  const categoryStore = useCategoryStore()

  const validateName = () => {
    if (!hasRange(name.value, 1, 20)) {
      nameError.value = 'Name must be between 1 and 20 characters'
      return false
    }
    nameError.value = ''
    return true
  }

  const handleClose = (emit) => {
    emit('close')
    name.value = ''
    color.value = '#16813D'
    nameError.value = ''
  }

  const handleSubmit = async (emit) => {
    if (!validateName()) {
      return
    }

    isLoading.value = true

    try {
      await categoryStore.addCategory(name.value, color.value)
      await categoryStore.fetchCategories()

      emit('close')

      name.value = ''
      color.value = '#16813D'
    } catch (error) {
      errorMessage.value = error.response?.data.message ? error.response.data.message : error.message
    } finally {
      isLoading.value = false
    }
  }

  const handleShowCategories = async () => {
    await categoryStore.fetchCategories()
    showCategories.value = !showCategories.value 
  }

  const handleDeleteCategory = async (categoryId) => {
    await categoryStore.deleteCategory(categoryId)
  }

  const confirmDeleteCategories = () => {
    if (selectedCategories.value.length === 0) {
      return; 
    }
    showDeleteConfirm.value = true;
  }

  const deleteSelectedCategories = async (emit) => {
    isLoading.value = true;
    try {
      await Promise.all(selectedCategories.value.map(categoryId => handleDeleteCategory(categoryId)));

      selectedCategories.value = [];

      await categoryStore.fetchCategories();
    } catch (error) {
      errorMessage.value = error.response?.data.message ? error.response.data.message : error.message;
    } finally {
      isLoading.value = false;
      showDeleteConfirm.value = false;
      emit('close');
      window.location.reload()
    }
  };

  const handleCancelDelete = () => {
    showDeleteConfirm.value = false;
  };

  const filteredCategories = computed(() => {
    if (!searchQuery.value) {
      return categoryStore.categories
    }
    return categoryStore.categories.filter(category =>
      category.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  })

  const paginatedCategories = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage
    const end = start + itemsPerPage
    return filteredCategories.value.slice(start, end)
  })

  const totalPages = computed(() => {
    return Math.ceil(filteredCategories.value.length / itemsPerPage)
  })

  const nextPage = () => {
    if (currentPage.value < totalPages.value) {
      currentPage.value++
    }
  }

  const prevPage = () => {
    if (currentPage.value > 1) {
      currentPage.value--
    }
  }

  const handleSearch = () => {
    currentPage.value = 1;
  }

  return {
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
  }
}
