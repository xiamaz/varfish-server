import { createPinia } from 'pinia'
import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'

import App from './App.vue'
const CohortList = () => import('./components/CohortList.vue')

import { useCohortsStore } from './stores/cohorts'

const routes = [
  {
    name: 'cohort-list',
    path: '/',
    component: CohortList,
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

const pinia = createPinia()
const app = createApp(App)
app.use(router)
app.use(pinia)
app.mount('#app')

const rawAppContext = JSON.parse(
  document.getElementById('sodar-ss-app-context').getAttribute('app-context') ||
    '{}'
)

const cohortsStore = useCohortsStore()
cohortsStore.initialize(rawAppContext)
