import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useConversationStore } from '../conversation'

describe('Conversation Store', () => {
  beforeEach(() => {
    // Create a fresh pinia instance for each test
    setActivePinia(createPinia())
  })

  describe('Initial State', () => {
    it('should have null sessionId initially', () => {
      const store = useConversationStore()
      expect(store.sessionId).toBeNull()
    })

    it('should have empty messages array initially', () => {
      const store = useConversationStore()
      expect(store.messages).toEqual([])
    })

    it('should not be loading initially', () => {
      const store = useConversationStore()
      expect(store.isLoading).toBe(false)
    })

    it('should have turnCount of 0 initially', () => {
      const store = useConversationStore()
      expect(store.turnCount).toBe(0)
    })

    it('should not have conversation initially', () => {
      const store = useConversationStore()
      expect(store.hasConversation).toBe(false)
    })
  })

  describe('startNewConversation', () => {
    it('should initialize a new conversation with language and scenario', () => {
      const store = useConversationStore()
      store.startNewConversation('japanese', 'restaurant')

      expect(store.sessionId).toBeTruthy()
      expect(store.language).toBe('japanese')
      expect(store.scenario).toBe('restaurant')
      expect(store.messages).toEqual([])
    })

    it('should generate unique session IDs', () => {
      const store = useConversationStore()
      store.startNewConversation('japanese', 'restaurant')
      const firstSessionId = store.sessionId

      store.startNewConversation('english', 'hotel')
      const secondSessionId = store.sessionId

      expect(firstSessionId).not.toBe(secondSessionId)
    })

    it('should reset messages when starting new conversation', () => {
      const store = useConversationStore()
      store.startNewConversation('japanese', 'restaurant')
      store.addMessage('user', 'Hello')

      expect(store.messages).toHaveLength(1)

      store.startNewConversation('english', 'hotel')

      expect(store.messages).toHaveLength(0)
    })
  })

  describe('addMessage', () => {
    it('should add user message to conversation', () => {
      const store = useConversationStore()
      store.startNewConversation('japanese', 'restaurant')
      store.addMessage('user', 'すみません')

      expect(store.messages).toHaveLength(1)
      expect(store.messages[0].role).toBe('user')
      expect(store.messages[0].content).toBe('すみません')
      expect(store.messages[0].timestamp).toBeTruthy()
    })

    it('should add assistant message to conversation', () => {
      const store = useConversationStore()
      store.startNewConversation('japanese', 'restaurant')
      store.addMessage('assistant', 'はい、どうぞ')

      expect(store.messages).toHaveLength(1)
      expect(store.messages[0].role).toBe('assistant')
      expect(store.messages[0].content).toBe('はい、どうぞ')
    })

    it('should maintain message order', () => {
      const store = useConversationStore()
      store.startNewConversation('japanese', 'restaurant')

      store.addMessage('user', 'Message 1')
      store.addMessage('assistant', 'Response 1')
      store.addMessage('user', 'Message 2')

      expect(store.messages).toHaveLength(3)
      expect(store.messages[0].content).toBe('Message 1')
      expect(store.messages[1].content).toBe('Response 1')
      expect(store.messages[2].content).toBe('Message 2')
    })
  })

  describe('Computed Properties', () => {
    it('should calculate turnCount correctly', () => {
      const store = useConversationStore()
      store.startNewConversation('japanese', 'restaurant')

      expect(store.turnCount).toBe(0)

      store.addMessage('user', 'Message 1')
      expect(store.turnCount).toBe(1)

      store.addMessage('assistant', 'Response 1')
      expect(store.turnCount).toBe(1)

      store.addMessage('user', 'Message 2')
      expect(store.turnCount).toBe(2)
    })

    it('should calculate hasConversation correctly', () => {
      const store = useConversationStore()

      expect(store.hasConversation).toBe(false)

      store.startNewConversation('japanese', 'restaurant')
      expect(store.hasConversation).toBe(false)

      store.addMessage('user', 'Hello')
      expect(store.hasConversation).toBe(true)
    })

    it('should filter userMessages correctly', () => {
      const store = useConversationStore()
      store.startNewConversation('japanese', 'restaurant')

      store.addMessage('user', 'Message 1')
      store.addMessage('assistant', 'Response 1')
      store.addMessage('user', 'Message 2')
      store.addMessage('assistant', 'Response 2')

      expect(store.userMessages).toHaveLength(2)
      expect(store.userMessages[0].content).toBe('Message 1')
      expect(store.userMessages[1].content).toBe('Message 2')
    })
  })

  describe('setLoading', () => {
    it('should set loading state to true', () => {
      const store = useConversationStore()
      store.setLoading(true)

      expect(store.isLoading).toBe(true)
    })

    it('should set loading state to false', () => {
      const store = useConversationStore()
      store.setLoading(true)
      store.setLoading(false)

      expect(store.isLoading).toBe(false)
    })
  })

  describe('resetConversation', () => {
    it('should reset all conversation data', () => {
      const store = useConversationStore()
      store.startNewConversation('japanese', 'restaurant')
      store.addMessage('user', 'Hello')
      store.setLoading(true)

      store.resetConversation()

      expect(store.sessionId).toBeNull()
      expect(store.language).toBeNull()
      expect(store.scenario).toBeNull()
      expect(store.messages).toEqual([])
      expect(store.isLoading).toBe(false)
    })
  })

  describe('getConversationData', () => {
    it('should return complete conversation data', () => {
      const store = useConversationStore()
      store.startNewConversation('japanese', 'restaurant')
      store.addMessage('user', 'Hello')

      const data = store.getConversationData()

      expect(data.sessionId).toBe(store.sessionId)
      expect(data.language).toBe('japanese')
      expect(data.scenario).toBe('restaurant')
      expect(data.messages).toHaveLength(1)
      expect(data.timestamp).toBeTruthy()
    })
  })
})
