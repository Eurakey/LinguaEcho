import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 30000 // 30 seconds
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
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
