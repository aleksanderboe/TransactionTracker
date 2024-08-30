import { defineStore } from 'pinia'
import axios from 'axios'
import { ref } from 'vue'

export const useCategoryStore = defineStore('categories', () => {
  const categories = ref([])

  const fetchCategories = async () => {
    const path = '/categories'

    const res = await axios.get(path, {
      headers: { Authorization: `Bearer ${localStorage.getItem('jwt')}` }
    })
    categories.value = res.data
  }

  const deleteCategory = async (category_id) => {
    const path = `/categories/${category_id}`

    await axios.delete(path, {
      headers: { Authorization: `Bearer ${localStorage.getItem('jwt')}` }
    })
    categories.value = categories.value.filter((category) => category.id !== category_id)
  }

  const addCategory = async (name, color) => {
    const res = await axios.post(
      '/categories',
      { name, color },
      {
        headers: { Authorization: `Bearer ${localStorage.getItem('jwt')}` }
      }
    )
    categories.value.push(res.data)
  }

  const updateCategory = async (category_id, name, color) => {
    const path = `/categories/${category_id}`
    const res = await axios.put(
      path,
      { name, color },
      {
        headers: { Authorization: `Bearer ${localStorage.getItem('jwt')}` }
      }
    )
    const index = categories.value.findIndex((category) => category.id === category_id)
    if (index !== -1) {
      categories.value[index] = res.data
    }
  }

  return {
    categories,
    fetchCategories,
    deleteCategory,
    addCategory,
    updateCategory
  }
})
