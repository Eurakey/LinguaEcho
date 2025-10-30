<template>
  <div class="report-page min-h-screen bg-gray-50 py-8">
    <div class="max-w-5xl mx-auto px-4">
      <!-- Header -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h1 class="text-3xl font-bold text-gray-800 mb-2">Conversation Report</h1>
            <p class="text-gray-600">Detailed feedback and analysis</p>
          </div>
          <div class="flex gap-2">
            <n-button @click="goToHistory">← History</n-button>
            <n-button @click="goHome" type="primary">New Conversation</n-button>
          </div>
        </div>

        <!-- Overview -->
        <div v-if="report" class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
          <div class="text-center p-4 bg-blue-50 rounded-lg">
            <p class="text-sm text-gray-600">Language</p>
            <p class="text-lg font-semibold text-blue-900">
              {{ report.overview.language }}
            </p>
          </div>
          <div class="text-center p-4 bg-green-50 rounded-lg">
            <p class="text-sm text-gray-600">Scenario</p>
            <p class="text-lg font-semibold text-green-900">
              {{ report.overview.scenario }}
            </p>
          </div>
          <div class="text-center p-4 bg-purple-50 rounded-lg">
            <p class="text-sm text-gray-600">Turns</p>
            <p class="text-lg font-semibold text-purple-900">
              {{ report.overview.turns }}
            </p>
          </div>
          <div class="text-center p-4 bg-orange-50 rounded-lg">
            <p class="text-sm text-gray-600">Words</p>
            <p class="text-lg font-semibold text-orange-900">
              {{ report.overview.word_count }}
            </p>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <n-spin size="large" />
        <p class="text-gray-600 mt-4">Loading report...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <p class="text-red-800 mb-4">{{ error }}</p>
        <n-button @click="goHome" type="primary">Go Home</n-button>
      </div>

      <!-- Report Content -->
      <div v-else-if="report" class="space-y-6">
        <!-- Positive Feedback -->
        <div class="bg-green-50 border-2 border-green-200 rounded-lg p-6">
          <h2 class="text-2xl font-bold text-green-900 mb-4 flex items-center">
            <span class="mr-2">✨</span>
            Great Job!
          </h2>
          <ul class="space-y-2">
            <li
              v-for="(feedback, index) in report.positive_feedback"
              :key="index"
              class="flex items-start"
            >
              <span class="text-green-600 mr-2">•</span>
              <span class="text-gray-800">{{ feedback }}</span>
            </li>
          </ul>
        </div>

        <!-- Grammar Errors -->
        <div v-if="report.grammar_errors.length > 0" class="bg-white rounded-lg shadow-sm p-6">
          <h2 class="text-2xl font-bold text-gray-800 mb-4 flex items-center">
            <span class="mr-2">📝</span>
            Grammar Analysis
            <n-tag :bordered="false" type="warning" class="ml-3">
              {{ report.grammar_errors.length }} {{ report.grammar_errors.length === 1 ? 'issue' : 'issues' }}
            </n-tag>
          </h2>
          <div class="space-y-4">
            <div
              v-for="(error, index) in report.grammar_errors"
              :key="index"
              class="border-l-4 border-yellow-400 pl-4 py-2"
            >
              <div class="mb-2">
                <span class="text-sm font-semibold text-gray-600">Error:</span>
                <span class="ml-2 text-red-600">{{ error.error }}</span>
              </div>
              <div class="mb-2">
                <span class="text-sm font-semibold text-gray-600">Correction:</span>
                <span class="ml-2 text-green-600">{{ error.correction }}</span>
              </div>
              <div class="mb-1">
                <span class="text-sm font-semibold text-gray-600">Explanation:</span>
                <p class="text-gray-700 mt-1">{{ error.explanation }}</p>
              </div>
              <div v-if="error.error_type">
                <n-tag size="small" type="info">{{ error.error_type }}</n-tag>
              </div>
            </div>
          </div>
        </div>

        <!-- Vocabulary Issues -->
        <div v-if="report.vocabulary_issues.length > 0" class="bg-white rounded-lg shadow-sm p-6">
          <h2 class="text-2xl font-bold text-gray-800 mb-4 flex items-center">
            <span class="mr-2">📚</span>
            Vocabulary Suggestions
            <n-tag :bordered="false" type="info" class="ml-3">
              {{ report.vocabulary_issues.length }}
            </n-tag>
          </h2>
          <div class="space-y-4">
            <div
              v-for="(issue, index) in report.vocabulary_issues"
              :key="index"
              class="border-l-4 border-blue-400 pl-4 py-2"
            >
              <div class="mb-2">
                <span class="text-sm font-semibold text-gray-600">You used:</span>
                <span class="ml-2 text-gray-800">{{ issue.original }}</span>
              </div>
              <div class="mb-2">
                <span class="text-sm font-semibold text-gray-600">Better choice:</span>
                <span class="ml-2 text-green-600 font-medium">{{ issue.suggestion }}</span>
              </div>
              <div>
                <span class="text-sm font-semibold text-gray-600">Why:</span>
                <p class="text-gray-700 mt-1">{{ issue.explanation }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Naturalness -->
        <div v-if="report.naturalness.length > 0" class="bg-white rounded-lg shadow-sm p-6">
          <h2 class="text-2xl font-bold text-gray-800 mb-4 flex items-center">
            <span class="mr-2">💬</span>
            Naturalness & Fluency
            <n-tag :bordered="false" type="success" class="ml-3">
              {{ report.naturalness.length }}
            </n-tag>
          </h2>
          <div class="space-y-4">
            <div
              v-for="(item, index) in report.naturalness"
              :key="index"
              class="border-l-4 border-purple-400 pl-4 py-2"
            >
              <div class="mb-2">
                <span class="text-sm font-semibold text-gray-600">Your expression:</span>
                <span class="ml-2 text-gray-800">{{ item.unnatural }}</span>
              </div>
              <div class="mb-2">
                <span class="text-sm font-semibold text-gray-600">More natural:</span>
                <span class="ml-2 text-green-600 font-medium">{{ item.natural }}</span>
              </div>
              <div>
                <span class="text-sm font-semibold text-gray-600">Note:</span>
                <p class="text-gray-700 mt-1">{{ item.context }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- No Issues -->
        <div
          v-if="report.grammar_errors.length === 0 &&
                report.vocabulary_issues.length === 0 &&
                report.naturalness.length === 0"
          class="bg-gradient-to-r from-green-50 to-blue-50 border-2 border-green-200 rounded-lg p-8 text-center"
        >
          <p class="text-3xl mb-4">🎉</p>
          <h3 class="text-2xl font-bold text-gray-800 mb-2">Perfect Conversation!</h3>
          <p class="text-gray-700">
            No errors detected. Your language usage was excellent!
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { NButton, NTag, NSpin } from 'naive-ui'
import { useHistoryStore } from '../stores/history'

const router = useRouter()
const route = useRoute()
const historyStore = useHistoryStore()

const report = ref(null)
const loading = ref(true)
const error = ref(null)

onMounted(() => {
  loadReport()
})

function loadReport() {
  try {
    // Load history from localStorage
    historyStore.loadHistory()

    // Get session ID from route params
    const sessionId = route.params.sessionId

    if (!sessionId) {
      error.value = 'No session ID provided'
      loading.value = false
      return
    }

    // Find conversation in history
    const conversation = historyStore.getConversationById(sessionId)

    if (!conversation || !conversation.report) {
      error.value = 'Report not found. Please generate a new report.'
      loading.value = false
      return
    }

    report.value = conversation.report
    loading.value = false
  } catch (e) {
    console.error('Error loading report:', e)
    error.value = 'Failed to load report'
    loading.value = false
  }
}

function goHome() {
  router.push('/')
}

function goToHistory() {
  router.push('/history')
}
</script>
