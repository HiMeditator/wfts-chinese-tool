<template>
<div class="comm">
  <h2>Communication Test</h2>
  <textarea v-model="text"></textarea>
  <br>
  <button @click="start">Start</button>
  <button @click="prompt">Prompt</button>
  <button @click="listen">Listen</button>
  <button @click="answer">Answer</button>
  <button @click="output">Output</button>
  <button @click="stop">Stop</button>
</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const text = ref('')

function start() {
  window.electron.ipcRenderer.send('server.start')
}

function prompt() {
  window.electron.ipcRenderer.send('server.prompt', text.value)
}

function listen() {
  window.electron.ipcRenderer.send('server.listen')
}

function answer() {
  window.electron.ipcRenderer.send('server.answer')
}

function output() {
  window.electron.ipcRenderer.send('server.output')
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
