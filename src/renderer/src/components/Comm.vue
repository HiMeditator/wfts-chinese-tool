<template>
<div class="comm">
  <h2>Communication Test</h2>
  <textarea v-model="text"></textarea>
  <br>
  <button @click="start">Start</button>
  <button @click="send">Send</button>
  <button @click="stop">Stop</button>
</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const text = ref('')

function start() {
  window.electron.ipcRenderer.send('server.start')
}

function send() {
  window.electron.ipcRenderer.send('server.send', text.value)
}

function stop() {
  window.electron.ipcRenderer.send('server.stop')
}
</script>

<style scoped>
.comm {
  padding: 20px;
}
button {
  margin-right: 10px;
}
</style>
