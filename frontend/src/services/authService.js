import api from './api'

/**
 * Authentication Service
 * Handles all authentication-related API calls
 */

export const authService = {
  /**
   * Register a new user
   */
  async register(email, password) {
    const response = await api.post('/api/auth/register', {
      email,
      password
    })
    return response.data
  },

  /**
   * Login with email and password
   */
  async login(email, password) {
    const response = await api.post('/api/auth/login', {
      email,
      password
    })
    return response.data
  },

  /**
   * Get current user information
   */
  async getCurrentUser() {
    const response = await api.get('/api/auth/me')
    return response.data
  },

  /**
   * Migrate localStorage conversations to database
   */
  async migrateData(conversations) {
    const response = await api.post('/api/migrate', {
      conversations
    })
    return response.data
  },

  /**
   * Get user's conversation history
   */
  async getConversations(limit = 50) {
    const response = await api.get('/api/conversations', {
      params: { limit }
    })
    return response.data
  },

  /**
   * Get specific conversation by session ID
   */
  async getConversation(sessionId) {
    const response = await api.get(`/api/conversations/${sessionId}`)
    return response.data
  },

  /**
   * Delete a conversation
   */
  async deleteConversation(conversationId) {
    await api.delete(`/api/conversations/${conversationId}`)
  }
}

export default authService
