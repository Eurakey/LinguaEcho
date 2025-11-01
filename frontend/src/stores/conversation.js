import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { v4 as uuidv4 } from 'uuid'

export const useConversationStore = defineStore('conversation', () => {
  // State
  const sessionId = ref(null)
  const language = ref(null)
  const scenario = ref(null)
  const messages = ref([])
  const isLoading = ref(false)

  // Streaming state
  const streamingContent = ref('')
  const isStreaming = ref(false)

  // Computed
  const userMessages = computed(() =>
    messages.value.filter(m => m.role === 'user')
  )

  const turnCount = computed(() => userMessages.value.length)

  const hasConversation = computed(() => messages.value.length > 0)

  // Actions
  function startNewConversation(selectedLanguage, selectedScenario) {
    sessionId.value = uuidv4()
    language.value = selectedLanguage
    scenario.value = selectedScenario
    messages.value = []
  }

  function addMessage(role, content) {
    messages.value.push({
      role,
      content,
      timestamp: new Date().toISOString()
    })
  }

  function setLoading(loading) {
    isLoading.value = loading
  }

  function setStreaming(streaming) {
    isStreaming.value = streaming
    if (!streaming) {
      streamingContent.value = ''
    }
  }

  function updateStreamingContent(content) {
    streamingContent.value += content
  }

  function resetConversation() {
    sessionId.value = null
    language.value = null
    scenario.value = null
    messages.value = []
    isLoading.value = false
    streamingContent.value = ''
    isStreaming.value = false
  }

  function getConversationData() {
    return {
      sessionId: sessionId.value,
      language: language.value,
      scenario: scenario.value,
      messages: messages.value,
      timestamp: new Date().toISOString()
    }
  }

  return {
    // State
    sessionId,
    language,
    scenario,
    messages,
    isLoading,
    // Streaming state
    streamingContent,
    isStreaming,
    // Computed
    userMessages,
    turnCount,
    hasConversation,
    // Actions
    startNewConversation,
    addMessage,
    setLoading,
    setStreaming,
    updateStreamingContent,
    resetConversation,
    getConversationData
  }
})
