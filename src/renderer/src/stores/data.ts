import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useDataStore = defineStore('data', () => {
  const status = ref('wait')
  const logs = ref([])

  return {
    status,
    logs
  }
})
