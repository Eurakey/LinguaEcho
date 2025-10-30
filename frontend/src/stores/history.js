import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useLocalStorage } from '../utils/localStorage'

const HISTORY_KEY = 'linguaecho_history'
const MAX_HISTORY_ITEMS = 10

export const useHistoryStore = defineStore('history', () => {
  const history = ref([])
  const localStorage = useLocalStorage()

  // Load history from localStorage on init
  function loadHistory() {
    const stored = localStorage.getItem(HISTORY_KEY)
    history.value = stored || []
  }

  // Save conversation to history
  function saveConversation(conversationData, report) {
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

  // Get conversation by ID
  function getConversationById(id) {
    return history.value.find(item => item.id === id)
  }

  // Delete conversation
  function deleteConversation(id) {
    history.value = history.value.filter(item => item.id !== id)
    localStorage.setItem(HISTORY_KEY, history.value)
  }

  // Clear all history
  function clearHistory() {
    history.value = []
    localStorage.removeItem(HISTORY_KEY)
  }

  return {
    history,
    loadHistory,
    saveConversation,
    getConversationById,
    deleteConversation,
    clearHistory
  }
})
