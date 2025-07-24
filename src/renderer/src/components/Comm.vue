<template>
<div class="comm">
  <a-textarea
    class="prompt-input"
    v-model:value="prompt"
    placeholder="输入系统提示词..."
  />
  <a-button size="small" type="primary" @click="send('start')">Start</a-button>
  <a-button size="small" type="primary" @click="send('prompt')">Prompt</a-button>
  <a-button size="small" type="primary" @click="send('listen')">Listen</a-button>
  <a-button size="small" type="primary" @click="send('answer')">Answer</a-button>
  <a-button size="small" type="primary" @click="send('output')">Output</a-button>
  <a-button size="small" type="primary" @click="send('stop')">Stop</a-button>
</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const prompt = ref('你需要扮演我的朋友 River 用英语和我对话。')

function send(cmd: string){
  if(cmd == 'prompt')
    window.electron.ipcRenderer.send(`server.${cmd}`, prompt.value)
  else
    window.electron.ipcRenderer.send(`server.${cmd}`)
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
