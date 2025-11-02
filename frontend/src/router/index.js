import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Conversation from '../views/Conversation.vue'
import Report from '../views/Report.vue'
import History from '../views/History.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/conversation',
      name: 'conversation',
      component: Conversation
    },
    {
      path: '/report/:sessionId',
      name: 'report',
      component: Report,
      props: true
    },
    {
      path: '/history',
      name: 'history',
      component: History
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    }
  ]
})

export default router
