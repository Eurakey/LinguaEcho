<template>
  <div class="conversation-page min-h-screen bg-gray-50">
    <!-- Sticky Header -->
    <div class="sticky top-0 z-50 bg-white shadow-sm border-b">
      <div class="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-gray-800">
            {{ scenarioTitle }}
          </h1>
          <p class="text-sm text-gray-600">
            {{ languageLabel }} • Turn {{ conversationStore.turnCount }}
          </p>
        </div>
        <div class="flex gap-2">
          <n-button @click="showEndDialog = true" type="warning">
            End Conversation
          </n-button>
          <n-button @click="goHome" quaternary>
            ← Home
          </n-button>
        </div>
      </div>
    </div>

    <!-- Chat Messages -->
    <div class="max-w-4xl mx-auto p-4 pt-6">
      <div class="space-y-4 mb-4" ref="messagesContainer">
        <!-- Welcome message -->
        <div v-if="conversationStore.messages.length === 0" class="text-center py-8">
          <p class="text-gray-600 mb-4">Start the conversation by typing a message below!</p>
          <p class="text-sm text-gray-500">The AI will respond in your target language.</p>
        </div>

        <!-- Messages -->
        <div
          v-for="(message, index) in conversationStore.messages"
          :key="index"
          :class="[
            'flex',
            message.role === 'user' ? 'justify-end' : 'justify-start'
          ]"
        >
          <div
            :class="[
              'max-w-[70%] rounded-lg px-4 py-3',
              message.role === 'user'
                ? 'bg-indigo-600 text-white'
                : 'bg-white shadow-sm border'
            ]"
          >
            <p class="whitespace-pre-wrap">{{ message.content }}</p>
            <p
              :class="[
                'text-xs mt-1',
                message.role === 'user' ? 'text-indigo-200' : 'text-gray-400'
              ]"
            >
              {{ formatTime(message.timestamp) }}
            </p>
          </div>
        </div>

        <!-- Loading indicator -->
        <div v-if="conversationStore.isLoading" class="flex justify-start">
          <div class="bg-white shadow-sm border rounded-lg px-4 py-3">
            <n-spin size="small" />
            <span class="ml-2 text-gray-600">AI is typing...</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="fixed bottom-0 left-0 right-0 bg-white border-t shadow-lg z-40">
      <div class="max-w-4xl mx-auto p-4">
        <div class="flex gap-2">
          <n-input
            v-model:value="userInput"
            type="textarea"
            :placeholder="`Type your message in ${languageLabel}...`"
            :autosize="{ minRows: 1, maxRows: 4 }"
            @keydown.enter.exact.prevent="sendMessage"
            :disabled="conversationStore.isLoading"
            clearable
          />
          <n-button
            type="primary"
            @click="sendMessage"
            :disabled="!userInput.trim() || conversationStore.isLoading"
            :loading="conversationStore.isLoading"
          >
            Send
          </n-button>
        </div>
        <div class="flex justify-between items-center">
          <p class="text-xs text-gray-500 mt-2">
            Press Enter to send • Shift+Enter for new line
          </p>
          <p v-if="userInput.length > 0" class="text-xs text-gray-500 mt-2">
            {{ userInput.length }} characters
          </p>
        </div>
      </div>
    </div>

    <!-- End Conversation Dialog -->
    <n-modal v-model:show="showEndDialog">
      <n-card
        style="width: 600px"
        title="End Conversation"
        :bordered="false"
        size="huge"
        role="dialog"
        aria-modal="true"
      >
        <p class="mb-4">
          Are you sure you want to end this conversation?
          A detailed feedback report will be generated.
        </p>
        <p class="text-sm text-gray-600 mb-4">
          Turns: {{ conversationStore.turnCount }}
        </p>
        <template #footer>
          <div class="flex justify-end gap-2">
            <n-button @click="showEndDialog = false">
              Cancel
            </n-button>
            <n-button
              type="primary"
              @click="endConversation"
              :loading="isGeneratingReport"
            >
              End & Generate Report
            </n-button>
          </div>
        </template>
      </n-card>
    </n-modal>

    <!-- Error Message -->
    <n-modal v-model:show="showError">
      <n-card
        style="width: 500px"
        title="Error"
        :bordered="false"
        size="huge"
      >
        <p class="text-red-600">{{ errorMessage }}</p>
        <template #footer>
          <n-button @click="showError = false">
            Close
          </n-button>
        </template>
      </n-card>
    </n-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { NButton, NInput, NModal, NCard, NSpin, useMessage } from 'naive-ui'
import { useConversationStore } from '../stores/conversation'
import { useHistoryStore } from '../stores/history'
import { sendChatMessage, generateReport } from '../services/api'
import { SCENARIO_INFO, LANGUAGE_LABELS } from '../utils/constants'

const router = useRouter()
const message = useMessage()
const conversationStore = useConversationStore()
const historyStore = useHistoryStore()

const userInput = ref('')
const showEndDialog = ref(false)
const showError = ref(false)
const errorMessage = ref('')
const isGeneratingReport = ref(false)
const messagesContainer = ref(null)

// Draft key for localStorage
const draftKey = computed(() => `draft-${conversationStore.sessionId}`)

// Auto-save draft
watch(userInput, (newVal) => {
  if (newVal.trim()) {
    localStorage.setItem(draftKey.value, newVal)
  } else {
    localStorage.removeItem(draftKey.value)
  }
})

// Computed
const scenarioTitle = computed(() => {
  if (!conversationStore.scenario || !conversationStore.language) return ''
  return SCENARIO_INFO[conversationStore.scenario]?.title[conversationStore.language] || ''
})

const languageLabel = computed(() => {
  return LANGUAGE_LABELS[conversationStore.language] || ''
})

// Methods
function formatTime(timestamp) {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}

async function sendMessage() {
  if (!userInput.value.trim() || conversationStore.isLoading) return

  const messageText = userInput.value.trim()
  userInput.value = ''
  localStorage.removeItem(draftKey.value) // Clear draft after sending

  try {
    // Add user message to store
    conversationStore.addMessage('user', messageText)
    conversationStore.setLoading(true)

    // Scroll to bottom
    await nextTick()
    scrollToBottom()

    // Prepare history for API
    const history = conversationStore.messages
      .slice(0, -1) // Exclude the message we just added
      .map(m => ({
        role: m.role,
        content: m.content
      }))

    // Send to API
    const response = await sendChatMessage(
      conversationStore.sessionId,
      conversationStore.language,
      conversationStore.scenario,
      messageText,
      history
    )

    // Add AI response
    conversationStore.addMessage('assistant', response.reply)

    // Scroll to bottom
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Error sending message:', error)
    // Show toast notification instead of modal
    message.error(error.message || 'Failed to send message. Please try again.')
    // Restore message to input for retry
    userInput.value = messageText
  } finally {
    conversationStore.setLoading(false)
  }
}

async function endConversation() {
  if (conversationStore.turnCount === 0) {
    message.warning('Please have at least one conversation turn before ending.')
    return
  }

  isGeneratingReport.value = true

  try {
    // Prepare conversation for report generation
    const conversation = conversationStore.messages.map(m => ({
      role: m.role,
      content: m.content
    }))

    // Generate report
    const response = await generateReport(
      conversationStore.sessionId,
      conversationStore.language,
      conversationStore.scenario,
      conversation
    )

    // Save to history
    historyStore.saveConversation(
      conversationStore.getConversationData(),
      response.report
    )

    // Navigate to report page
    router.push(`/report/${conversationStore.sessionId}`)
  } catch (error) {
    console.error('Error generating report:', error)
    errorMessage.value = error.message || 'Failed to generate report. Please try again.'
    showError.value = true
  } finally {
    isGeneratingReport.value = false
    showEndDialog.value = false
  }
}

function goHome() {
  if (conversationStore.hasConversation) {
    if (confirm('Are you sure you want to leave? Your conversation will not be saved.')) {
      conversationStore.resetConversation()
      router.push('/')
    }
  } else {
    router.push('/')
  }
}

function scrollToBottom() {
  if (messagesContainer.value) {
    const container = messagesContainer.value
    container.scrollTop = container.scrollHeight
  }
}

// Lifecycle
onMounted(() => {
  // Redirect if no active conversation
  if (!conversationStore.sessionId) {
    router.push('/')
    return
  }

  // Load draft from localStorage
  const savedDraft = localStorage.getItem(draftKey.value)
  if (savedDraft) {
    userInput.value = savedDraft
  }

  // Load history store
  historyStore.loadHistory()

  // Auto-scroll on new messages
  watch(
    () => conversationStore.messages.length,
    async () => {
      await nextTick()
      scrollToBottom()
    }
  )
})
</script>

<style scoped>
.conversation-page {
  padding-bottom: 120px; /* Space for fixed input */
}
</style>
