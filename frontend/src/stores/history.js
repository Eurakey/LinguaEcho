import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useLocalStorage } from '../utils/localStorage'
import { useAuthStore } from './auth'
import authService from '../services/authService'

const HISTORY_KEY = 'linguaecho_history'
const MAX_HISTORY_ITEMS = 10

export const useHistoryStore = defineStore('history', () => {
  const history = ref([])
  const localStorage = useLocalStorage()
  const isLoading = ref(false)

  // Load history - dual mode (localStorage for guests, API for authenticated users)
  async function loadHistory() {
    const authStore = useAuthStore()
    isLoading.value = true

    try {
      if (authStore.isLoggedIn) {
        // Authenticated: fetch from API
        const conversations = await authService.getConversations(MAX_HISTORY_ITEMS)

        // Transform API data to match localStorage format
        history.value = conversations.map(conv => ({
          id: conv.session_id,
          language: conv.language,
          scenario: conv.scenario,
          messages: conv.messages || [],
          report: conv.report || null,
          timestamp: conv.created_at
        }))
      } else {
        // Guest: load from localStorage
        const stored = localStorage.getItem(HISTORY_KEY)
        history.value = stored || []
      }
    } catch (error) {
      console.error('Failed to load history:', error)
      // Fallback to localStorage on error
      const stored = localStorage.getItem(HISTORY_KEY)
      history.value = stored || []
    } finally {
      isLoading.value = false
    }
  }

  // Save conversation to history (only for guest mode, authenticated users auto-save via API)
  function saveConversation(conversationData, report) {
    const authStore = useAuthStore()

    // Only save to localStorage if user is NOT authenticated
    // Authenticated users' data is saved automatically via API
    if (!authStore.isLoggedIn) {
      const historyItem = {
        id: conversationData.sessionId,
        language: conversationData.language,
        scenario: conversationData.scenario,
        messages: conversationData.messages,
        report: report,
        timestamp: new Date().toISOString()
      }

      // Add to beginning of history
      history.value.unshift(historyItem)

      // Keep only last MAX_HISTORY_ITEMS
      if (history.value.length > MAX_HISTORY_ITEMS) {
        history.value = history.value.slice(0, MAX_HISTORY_ITEMS)
      }

      // Save to localStorage
      localStorage.setItem(HISTORY_KEY, history.value)
    }
  }

  // Get conversation by ID
  function getConversationById(id) {
    return history.value.find(item => item.id === id)
  }

  // Delete conversation
  async function deleteConversation(id) {
    const authStore = useAuthStore()

    if (authStore.isLoggedIn) {
      // Authenticated: delete via API
      try {
        await authService.deleteConversation(id)
        history.value = history.value.filter(item => item.id !== id)
      } catch (error) {
        console.error('Failed to delete conversation:', error)
        throw error
      }
    } else {
      // Guest: delete from localStorage
      history.value = history.value.filter(item => item.id !== id)
      localStorage.setItem(HISTORY_KEY, history.value)
    }
  }

  // Clear all history (localStorage only)
  function clearHistory() {
    history.value = []
    localStorage.removeItem(HISTORY_KEY)
  }

  // Get all conversations (for migration)
  function getAllConversations() {
    const stored = localStorage.getItem(HISTORY_KEY)
    return stored || []
  }

  // Clear all localStorage conversations (after migration)
  function clearAllConversations() {
    localStorage.removeItem(HISTORY_KEY)
    history.value = []
  }

  return {
    history,
    isLoading,
    loadHistory,
    saveConversation,
    getConversationById,
    deleteConversation,
    clearHistory,
    getAllConversations,
    clearAllConversations
  }
})
