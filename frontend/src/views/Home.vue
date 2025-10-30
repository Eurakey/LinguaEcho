<template>
  <div class="home-page min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-12 pt-8">
        <h1 class="text-5xl font-bold text-indigo-900 mb-4">LinguaEcho</h1>
        <p class="text-xl text-gray-700">AI-Powered Language Learning Through Conversation</p>
        <div class="mt-4">
          <n-button text tag="a" @click="$router.push('/history')" class="text-indigo-600">
            View History →
          </n-button>
        </div>
      </div>

      <!-- Step 1: Language Selection -->
      <div class="mb-12">
        <h2 class="text-2xl font-semibold text-gray-800 mb-6 text-center">
          Step 1: Choose Your Language
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-2xl mx-auto">
          <n-card
            v-for="lang in languages"
            :key="lang.value"
            :class="[
              'cursor-pointer transition-all hover:shadow-xl',
              selectedLanguage === lang.value ? 'ring-4 ring-indigo-500' : ''
            ]"
            @click="selectLanguage(lang.value)"
          >
            <div class="text-center py-4">
              <div class="text-4xl mb-3">{{ lang.icon }}</div>
              <h3 class="text-2xl font-semibold mb-2">{{ lang.label }}</h3>
              <p class="text-gray-600">{{ lang.description }}</p>
            </div>
          </n-card>
        </div>
      </div>

      <!-- Step 2: Scenario Selection -->
      <div v-if="selectedLanguage" class="mb-12">
        <h2 class="text-2xl font-semibold text-gray-800 mb-6 text-center">
          Step 2: Choose a Scenario
        </h2>

        <!-- Scenarios by category -->
        <div v-for="category in categories" :key="category" class="mb-8">
          <h3 class="text-xl font-semibold text-gray-700 mb-4 px-2">
            {{ getCategoryLabel(category) }}
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <n-card
              v-for="scenario in getScenariosByCategory(category)"
              :key="scenario.key"
              :class="[
                'cursor-pointer transition-all hover:shadow-lg',
                selectedScenario === scenario.key ? 'ring-4 ring-indigo-500' : ''
              ]"
              @click="selectScenario(scenario.key)"
            >
              <div class="py-2">
                <h4 class="text-lg font-semibold mb-2">{{ scenario.title }}</h4>
                <p class="text-sm text-gray-600">{{ scenario.description }}</p>
              </div>
            </n-card>
          </div>
        </div>

        <!-- Start Button -->
        <div class="text-center mt-12">
          <n-button
            type="primary"
            size="large"
            :disabled="!selectedScenario"
            @click="startConversation"
            class="px-12 py-3 text-lg"
          >
            Start Conversation →
          </n-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { NCard, NButton } from 'naive-ui'
import { useConversationStore } from '../stores/conversation'
import { LANGUAGES, LANGUAGE_LABELS, SCENARIOS, SCENARIO_INFO, CATEGORY_LABELS } from '../utils/constants'

const router = useRouter()
const conversationStore = useConversationStore()

const selectedLanguage = ref(null)
const selectedScenario = ref(null)

const languages = [
  {
    value: LANGUAGES.JAPANESE,
    label: 'Japanese',
    description: '日本語で会話練習',
    icon: '🇯🇵'
  },
  {
    value: LANGUAGES.ENGLISH,
    label: 'English',
    description: 'Practice in English',
    icon: '🇺🇸'
  }
]

const categories = ['daily', 'social', 'professional']

function getCategoryLabel(category) {
  return CATEGORY_LABELS[category][selectedLanguage.value] || category
}

function getScenariosByCategory(category) {
  return Object.entries(SCENARIO_INFO)
    .filter(([_, info]) => info.category === category)
    .map(([key, info]) => ({
      key,
      title: info.title[selectedLanguage.value],
      description: info.description[selectedLanguage.value]
    }))
}

function selectLanguage(lang) {
  selectedLanguage.value = lang
  selectedScenario.value = null // Reset scenario when language changes
}

function selectScenario(scenario) {
  selectedScenario.value = scenario
}

function startConversation() {
  if (selectedLanguage.value && selectedScenario.value) {
    conversationStore.startNewConversation(selectedLanguage.value, selectedScenario.value)
    router.push('/conversation')
  }
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
}
</style>
