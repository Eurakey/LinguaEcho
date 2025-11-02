import { defineStore } from 'pinia'
import authService from '../services/authService'

/**
 * Authentication Store
 * Manages user authentication state
 */
export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('auth_token') || null,
    isAuthenticated: false,
    isLoading: false,
    error: null
  }),

  getters: {
    /**
     * Check if user is logged in
     */
    isLoggedIn: (state) => state.isAuthenticated && state.token !== null,

    /**
     * Get user email
     */
    userEmail: (state) => state.user?.email || null
  },

  actions: {
    /**
     * Initialize auth state from localStorage
     */
    async initialize() {
      if (this.token) {
        try {
          await this.fetchCurrentUser()
        } catch (error) {
          // Token is invalid, clear it
          this.logout()
        }
      }
    },

    /**
     * Register new user
     */
    async register(email, password) {
      this.isLoading = true
      this.error = null

      try {
        const data = await authService.register(email, password)
        this.setAuthData(data.access_token)
        await this.fetchCurrentUser()
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Registration failed'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    /**
     * Login user
     */
    async login(email, password) {
      this.isLoading = true
      this.error = null

      try {
        const data = await authService.login(email, password)
        this.setAuthData(data.access_token)
        await this.fetchCurrentUser()
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Login failed'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    /**
     * Logout user
     */
    logout() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      localStorage.removeItem('auth_token')
    },

    /**
     * Fetch current user information
     */
    async fetchCurrentUser() {
      try {
        const userData = await authService.getCurrentUser()
        this.user = userData
        this.isAuthenticated = true
      } catch (error) {
        console.error('Failed to fetch user:', error)
        throw error
      }
    },

    /**
     * Set authentication data
     */
    setAuthData(token) {
      this.token = token
      localStorage.setItem('auth_token', token)
    },

    /**
     * Migrate localStorage conversations to database
     */
    async migrateLocalData(conversations) {
      try {
        const result = await authService.migrateData(conversations)
        return result
      } catch (error) {
        console.error('Migration failed:', error)
        throw error
      }
    }
  }
})
