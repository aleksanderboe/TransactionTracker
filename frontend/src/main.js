import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css'

axios.defaults.baseURL = import.meta.env.VITE_APP_API_URL

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
