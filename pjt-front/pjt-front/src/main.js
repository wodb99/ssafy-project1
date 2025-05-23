import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import App from './App.vue'
import router from './router'

const app = createApp(App)

// Pinia 생성 및 플러그인 적용
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

// 전역 등록
app.use(pinia)
app.use(router)

app.mount('#app')