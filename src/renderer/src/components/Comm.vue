<template>
  <div class="comm">
    <a-row>
      <a-col :span="10">
        <a-statistic title="Status" :value="status" :value-style="{fontSize:'16px'}"/>
      </a-col>
      <a-col :span="7">
        <a-statistic title="Messages" :value="messages.length" :value-style="{fontSize:'16px'}"/>
      </a-col>
      <a-col :span="7">
        <a-statistic title="Logs" :value="logs.length" :value-style="{fontSize:'16px'}"/>
      </a-col>
    </a-row>
    <a-textarea
      class="prompt-input"
      v-model:value="prompt"
      placeholder="输入系统提示词..."
    />
    <div class="main-control">
      <template v-if="command === 'Stopped'">
        <a-button size="small" type="primary" @click="send('start')">Start</a-button>
      </template>
      <template v-else>
        <a-button size="small" danger ghost @click="send('stop')">Stop</a-button>
      </template>
      <a-button
        size="small" type="primary" @click="send('prompt')"
        :disabled="status === 'stopped'"
      >Prompt</a-button>
      <a-button
        size="small" type="primary" @click="send('')"
        :loading="command === 'Pending'"
        :disabled="command === 'Pending' || command === 'Stopped'"
      >{{ command }}</a-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { storeToRefs } from 'pinia';
import { useDataStore } from '@renderer/stores/data'

const dataStore = useDataStore()
const { status, messages, logs, command } = storeToRefs(dataStore)
const prompt = ref('你需要扮演我的朋友 River 用英语和我对话。')

function send(cmd: string){
  if(cmd === '') { cmd = command.value.toLowerCase() }
  if(cmd == 'prompt')
    window.electron.ipcRenderer.send(`server.${cmd}`, prompt.value)
  else
    window.electron.ipcRenderer.send(`server.${cmd}`)
}
</script>

<style scoped>
.comm {
  margin: 12px;
  display: flex;
  flex-direction: column;
}

.stat {
  font-size: 12px !important;
}

.prompt-input {
  display: block;
  margin: 10px 0;
}

.main-control {
  margin-top: 10px;
  display: flex;
  justify-content: center;
}

.status-tag {
  padding: 3px;
}

button {
  margin-right: 10px;
  min-width: 60px;
}
</style>
