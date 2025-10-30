<template>
  <div class="history-page min-h-screen bg-gray-50 py-8">
    <div class="max-w-6xl mx-auto px-4">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-800 mb-2">Conversation History</h1>
          <p class="text-gray-600">Review your past conversations and reports</p>
        </div>
        <div class="flex gap-2">
          <n-button @click="goHome">← Home</n-button>
          <n-button
            v-if="historyStore.history.length > 0"
            @click="showClearConfirm = true"
            type="error"
            secondary
          >
            Clear All
          </n-button>
        </div>
      </div>

      <!-- Empty State -->
      <div
        v-if="historyStore.history.length === 0"
        class="bg-white rounded-lg shadow-sm p-12 text-center"
      >
        <p class="text-5xl mb-4">📚</p>
        <h2 class="text-2xl font-semibold text-gray-800 mb-2">No conversations yet</h2>
        <p class="text-gray-600 mb-6">
          Start a new conversation to see your history here
        </p>
        <n-button type="primary" size="large" @click="goHome">
          Start Learning
        </n-button>
      </div>

      <!-- History List -->
      <div v-else class="space-y-4">
        <n-card
          v-for="item in historyStore.history"
          :key="item.id"
          class="hover:shadow-lg transition-shadow cursor-pointer"
          @click="viewReport(item.id)"
        >
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <!-- Title -->
              <div class="flex items-center gap-3 mb-2">
                <h3 class="text-xl font-semibold text-gray-800">
                  {{ getScenarioTitle(item.scenario, item.language) }}
                </h3>
                <n-tag :type="getLanguageTagType(item.language)" size="small">
                  {{ item.language }}
                </n-tag>
              </div>

              <!-- Metadata -->
              <div class="flex flex-wrap gap-4 text-sm text-gray-600 mb-3">
                <span>📅 {{ formatDate(item.timestamp) }}</span>
                <span>💬 {{ getUserMessageCount(item.messages) }} turns</span>
                <span>📊 {{ getTotalWords(item.messages) }} words</span>
              </div>

              <!-- Stats -->
              <div class="flex gap-2">
                <n-tag
                  v-if="item.report.grammar_errors.length > 0"
                  size="small"
                  type="warning"
                  :bordered="false"
                >
                  {{ item.report.grammar_errors.length }} grammar
                </n-tag>
                <n-tag
                  v-if="item.report.vocabulary_issues.length > 0"
                  size="small"
                  type="info"
                  :bordered="false"
                >
                  {{ item.report.vocabulary_issues.length }} vocabulary
                </n-tag>
                <n-tag
                  v-if="item.report.naturalness.length > 0"
                  size="small"
                  type="success"
                  :bordered="false"
                >
                  {{ item.report.naturalness.length }} naturalness
                </n-tag>
                <n-tag
                  v-if="item.report.grammar_errors.length === 0 &&
                        item.report.vocabulary_issues.length === 0 &&
                        item.report.naturalness.length === 0"
                  size="small"
                  type="success"
                  :bordered="false"
                >
                  ✨ Perfect
                </n-tag>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex gap-2 ml-4">
              <n-button
                size="small"
                @click.stop="viewReport(item.id)"
                type="primary"
                secondary
              >
                View Report
              </n-button>
              <n-button
                size="small"
                @click.stop="confirmDelete(item.id)"
                type="error"
                quaternary
              >
                Delete
              </n-button>
            </div>
          </div>
        </n-card>
      </div>

      <!-- Clear All Confirmation -->
      <n-modal v-model:show="showClearConfirm">
        <n-card
          style="width: 500px"
          title="Clear All History"
          :bordered="false"
          size="huge"
        >
          <p class="mb-4">
            Are you sure you want to delete all conversation history?
            This action cannot be undone.
          </p>
          <template #footer>
            <div class="flex justify-end gap-2">
              <n-button @click="showClearConfirm = false">
                Cancel
              </n-button>
              <n-button type="error" @click="clearAllHistory">
                Clear All
              </n-button>
            </div>
          </template>
        </n-card>
      </n-modal>

      <!-- Delete Confirmation -->
      <n-modal v-model:show="showDeleteConfirm">
        <n-card
          style="width: 500px"
          title="Delete Conversation"
          :bordered="false"
          size="huge"
        >
          <p>Are you sure you want to delete this conversation?</p>
          <template #footer>
            <div class="flex justify-end gap-2">
              <n-button @click="showDeleteConfirm = false">
                Cancel
              </n-button>
              <n-button type="error" @click="deleteConversation">
                Delete
              </n-button>
            </div>
          </template>
        </n-card>
      </n-modal>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { NCard, NButton, NTag, NModal, useMessage } from 'naive-ui'
import { useHistoryStore } from '../stores/history'
import { SCENARIO_INFO } from '../utils/constants'

const router = useRouter()
const message = useMessage()
const historyStore = useHistoryStore()

const showClearConfirm = ref(false)
const showDeleteConfirm = ref(false)
const deleteTargetId = ref(null)

onMounted(() => {
  historyStore.loadHistory()
})

function getScenarioTitle(scenario, language) {
  return SCENARIO_INFO[scenario]?.title[language] || scenario
}

function getLanguageTagType(language) {
  return language === 'japanese' ? 'error' : 'info'
}

function getUserMessageCount(messages) {
  return messages.filter(m => m.role === 'user').length
}

function getTotalWords(messages) {
  return messages
    .filter(m => m.role === 'user')
    .reduce((total, m) => total + m.content.split(/\s+/).length, 0)
}

function formatDate(timestamp) {
  const date = new Date(timestamp)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 1) {
    return 'Today'
  } else if (diffDays === 2) {
    return 'Yesterday'
  } else if (diffDays <= 7) {
    return `${diffDays - 1} days ago`
  } else {
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }
}

function viewReport(id) {
  router.push(`/report/${id}`)
}

function confirmDelete(id) {
  deleteTargetId.value = id
  showDeleteConfirm.value = true
}

function deleteConversation() {
  if (deleteTargetId.value) {
    historyStore.deleteConversation(deleteTargetId.value)
    message.success('Conversation deleted')
    showDeleteConfirm.value = false
    deleteTargetId.value = null
  }
}

function clearAllHistory() {
  historyStore.clearHistory()
  message.success('All history cleared')
  showClearConfirm.value = false
}

function goHome() {
  router.push('/')
}
</script>
