<template>
  <div class="all-logs">
    <div v-for="(log, idx) in logs" :key="idx" :class="[log.type]">
      {{ log.content }}
    </div>
  </div>
</template>

<script setup lang="ts">
// import { ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useDataStore } from '@renderer/stores/data'

const dataStore = useDataStore()
const { logs } = storeToRefs(dataStore)
</script>

<style scoped>
.all-logs {
  margin: 12px;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  scrollbar-width: none;
  background-color:antiquewhite;
}

.info, .warn, .error {
  font-size: 12px;
  line-height: 3em;
}

.info:hover, .warn:hover, .error:hover {
  background-color: #aaa2;
}

.warn {
  color: #faad14;
}

.error {
  color: #ff4d4f;
}
</style>
