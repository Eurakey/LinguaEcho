/**
 * localStorage wrapper utility
 */

export function useLocalStorage() {
  const isAvailable = () => {
    try {
      const test = '__localStorage_test__'
      localStorage.setItem(test, test)
      localStorage.removeItem(test)
      return true
    } catch (e) {
      return false
    }
  }

  const getItem = (key) => {
    if (!isAvailable()) return null

    try {
      const item = localStorage.getItem(key)
      return item ? JSON.parse(item) : null
    } catch (e) {
      console.error('Error reading from localStorage:', e)
      return null
    }
  }

  const setItem = (key, value) => {
    if (!isAvailable()) return false

    try {
      localStorage.setItem(key, JSON.stringify(value))
      return true
    } catch (e) {
      console.error('Error writing to localStorage:', e)
      return false
    }
  }

  const removeItem = (key) => {
    if (!isAvailable()) return

    try {
      localStorage.removeItem(key)
    } catch (e) {
      console.error('Error removing from localStorage:', e)
    }
  }

  const clear = () => {
    if (!isAvailable()) return

    try {
      localStorage.clear()
    } catch (e) {
      console.error('Error clearing localStorage:', e)
    }
  }

  return {
    getItem,
    setItem,
    removeItem,
    clear,
    isAvailable
  }
}
