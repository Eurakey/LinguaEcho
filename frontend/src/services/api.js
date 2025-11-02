import axios from 'axios'
import { SSEClient } from './sse'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 30000 // 30 seconds
})

// Request interceptor - add JWT token if available
apiClient.interceptors.request.use(
  (config) => {
    // Get token from localStorage
    const token = localStorage.getItem('auth_token')

    // Add Authorization header if token exists
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response) {
      // Server responded with error status
      console.error('API Error:', error.response.data)

      // Handle 401 Unauthorized - token expired or invalid
      if (error.response.status === 401) {
        // Clear invalid token
        localStorage.removeItem('auth_token')
        // Optionally redirect to login page
        // This can be handled by the auth store instead
      }
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error:', error.message)
    } else {
      // Something else happened
      console.error('Error:', error.message)
    }
    return Promise.reject(error)
  }
)

/**
 * Send a chat message and get AI response
 */
export async function sendChatMessage(sessionId, language, scenario, message, history) {
  try {
    const response = await apiClient.post('/api/chat', {
      session_id: sessionId,
      language,
      scenario,
      message,
      history
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to send message')
  }
}

/**
 * Send a chat message with streaming response
 * @returns {AsyncGenerator} - Async generator that yields SSE events
 */
export async function* sendChatMessageStream(sessionId, language, scenario, message, history) {
  const url = `${API_BASE_URL}/api/chat/stream`

  const requestBody = {
    session_id: sessionId,
    language,
    scenario,
    message,
    history
  }

  const client = new SSEClient(url)

  try {
    for await (const event of client.stream(requestBody)) {
      yield event
    }
  } catch (error) {
    console.error('SSE streaming error:', error)
    throw new Error(error.message || 'Failed to stream message')
  }
}

/**
 * Generate conversation report
 */
export async function generateReport(sessionId, language, scenario, conversation) {
  try {
    const response = await apiClient.post('/api/report/generate', {
      session_id: sessionId,
      language,
      scenario,
      conversation
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to generate report')
  }
}

/**
 * Health check
 */
export async function checkHealth() {
  try {
    const response = await apiClient.get('/health')
    return response.data
  } catch (error) {
    throw new Error('API health check failed')
  }
}

export default apiClient
