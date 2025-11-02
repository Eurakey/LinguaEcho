<template>
  <header class="app-header">
    <div class="header-content">
      <!-- Logo -->
      <div class="logo">
        <router-link to="/">
          <h1>🗣️ LinguaEcho</h1>
        </router-link>
      </div>

      <!-- Navigation & Auth -->
      <div class="header-right">
        <nav class="nav-links">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link to="/history" class="nav-link">History</router-link>
        </nav>

        <!-- User Info & Auth Buttons -->
        <div v-if="authStore.isLoggedIn" class="user-section">
          <span class="user-email">{{ authStore.userEmail }}</span>
          <button @click="handleLogout" class="btn-logout">
            Logout
          </button>
        </div>
        <div v-else class="auth-buttons">
          <router-link to="/login" class="btn-login">Login</router-link>
          <router-link to="/register" class="btn-register">Register</router-link>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo a {
  text-decoration: none;
}

.logo h1 {
  color: white;
  font-size: 24px;
  font-weight: 700;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 24px;
}

.nav-links {
  display: flex;
  gap: 16px;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.nav-link.router-link-active {
  background-color: rgba(255, 255, 255, 0.3);
}

.user-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-email {
  color: white;
  font-weight: 500;
  background-color: rgba(255, 255, 255, 0.2);
  padding: 8px 16px;
  border-radius: 8px;
}

.btn-logout {
  background-color: rgba(255, 255, 255, 0.9);
  color: #667eea;
  border: none;
  padding: 8px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-logout:hover {
  background-color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.auth-buttons {
  display: flex;
  gap: 12px;
}

.btn-login,
.btn-register {
  padding: 8px 20px;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
}

.btn-login {
  color: white;
  background-color: rgba(255, 255, 255, 0.2);
}

.btn-login:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.btn-register {
  background-color: white;
  color: #667eea;
}

.btn-register:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
    padding: 12px 16px;
  }

  .header-right {
    flex-direction: column;
    gap: 12px;
    width: 100%;
  }

  .nav-links {
    width: 100%;
    justify-content: center;
  }

  .user-section,
  .auth-buttons {
    width: 100%;
    justify-content: center;
  }

  .user-email {
    font-size: 14px;
  }
}
</style>
