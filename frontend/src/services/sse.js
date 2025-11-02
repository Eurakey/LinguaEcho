/**
 * SSE (Server-Sent Events) Client using fetch API with ReadableStream
 * Supports POST requests with JSON body for streaming responses
 */

export class SSEClient {
  constructor(url, options = {}) {
    this.url = url
    this.options = options
    this.controller = null
  }

  /**
   * Stream data from SSE endpoint
   * @param {Object} requestBody - Request body to send
   * @yields {Object} - Parsed SSE event data
   */
  async *stream(requestBody) {
    this.controller = new AbortController()

    try {
      // Get auth token from localStorage
      const token = localStorage.getItem('auth_token')
      const headers = {
        'Content-Type': 'application/json',
        ...this.options.headers,
      }

      // Add Authorization header if token exists
      if (token) {
        headers.Authorization = `Bearer ${token}`
      }

      const response = await fetch(this.url, {
        method: 'POST',
        headers,
        body: JSON.stringify(requestBody),
        signal: this.controller.signal,
      })

      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()

        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')

        // Keep last incomplete line in buffer
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              yield data
            } catch (error) {
              console.error('Failed to parse SSE data:', line, error)
            }
          }
        }
      }
    } catch (error) {
      if (error.name === 'AbortError') {
        console.log('SSE connection aborted by client')
      } else {
        console.error('SSE streaming error:', error)
        throw error
      }
    }
  }

  /**
   * Cancel the ongoing SSE connection
   */
  cancel() {
    if (this.controller) {
      this.controller.abort()
      this.controller = null
    }
  }
}
