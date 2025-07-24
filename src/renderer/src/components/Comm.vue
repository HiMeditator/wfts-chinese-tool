<template>
<div class="comm">
  <a-textarea
    class="prompt-input"
    v-model:value="text"
    placeholder="输入系统提示词..."
  />
  <a-button size="small" type="primary" @click="start">Start</a-button>
  <a-button size="small" type="primary" @click="prompt">Prompt</a-button>
  <a-button size="small" type="primary" @click="listen">Listen</a-button>
  <a-button size="small" type="primary" @click="answer">Answer</a-button>
  <a-button size="small" type="primary" @click="output">Output</a-button>
  <a-button size="small" type="primary" @click="stop">Stop</a-button>
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
  padding: 12px;
}

.prompt-input {
  display: block;
  margin-bottom: 10px;
}

</style>
