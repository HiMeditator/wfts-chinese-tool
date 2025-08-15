<template>
  <div class="comm">
    <a-row>
      <a-col :span="8">
        <a-statistic title="状态" :value="status_zh" :value-style="{fontSize:'16px'}"/>
      </a-col>
      <a-col :span="8">
        <a-statistic title="消息数" :value="messages.length" :value-style="{fontSize:'16px'}"/>
      </a-col>
      <a-col :span="8">
        <a-statistic title="日志数" :value="logs.length" :value-style="{fontSize:'16px'}"/>
      </a-col>
    </a-row>
    <a-row>
      <a-col :span="12">
        <a-textarea
          ref="textarea1"
          class="prompt-input"
          v-model:value="answer_zh"
          :disabled="status === 'recording'"
          placeholder="中文回答"
          :auto-size="{ minRows: 3, maxRows: 5 }"
        />
      </a-col>
      <a-col :span="12">
        <a-textarea
          ref="textarea2"
          class="prompt-input"
          v-model:value="answer_en"
          :disabled="status === 'recording'"
          placeholder="英文翻译"
          :auto-size="{ minRows: 3, maxRows: 5 }"
        />
      </a-col>
    </a-row>
    <div class="main-control">
      <template v-if="status === 'stopped'">
        <a-button size="small" type="primary" @click="send('start')">启动</a-button>
      </template>
      <template v-else>
        <a-button size="small" danger ghost
          @click="send('stop')"
          :disabled="status === 'connecting'"
        >停止</a-button>
      </template>

      <a-button v-if="status === 'listening'"
        size="small" danger ghost @click="send('break')"
      >停止监听</a-button>
      <a-button v-else
        size="small" type="primary" @click="send('listen')"
        :disabled="status !== 'ready'"
      >语音监听</a-button>

      <a-button v-if="status === 'recording'"
        size="small" danger ghost @click="send('break')"
      >停止输入</a-button>
      <a-button v-else
        size="small" type="primary" @click="send('record')"
        :disabled="status !== 'ready'"
      >语音输入</a-button>
    </div>
    <div class="main-control">
    <a-popover title="翻译选项">
      <template #content>
        <div style="margin-bottom: 10px;">
          <span class="label">模型选项</span>
          <a-radio-group v-model:value="modelType">
            <a-radio-button value="remote">云端模型</a-radio-button>
            <a-radio-button value="ollama">Ollama模型</a-radio-button>
          </a-radio-group>          
        </div>
        <div>
          <span class="label">模型名称</span>
          <a-input
            v-model:value="modelName" placeholder="模型名称"
            style="width: 190px;"
          />          
        </div>
      </template>
      <a-button
        size="small" type="primary" @click="send('translate')"
        :disabled="status !== 'ready'"
        :loading="status === 'translating'"
      >翻译为英语</a-button>
      </a-popover>
      <a-button
        size="small" type="primary" @click="send('synthesis')"
        :disabled="status !== 'ready'"
        :loading="status === 'synthesising'"
      >音频合成</a-button>
      <a-button
        size="small" type="primary" @click="send('output')"
        :disabled="status !== 'ready'"
        :loading="status === 'outputting'"
      >音频输出</a-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { storeToRefs } from 'pinia';
import { useDataStore } from '@renderer/stores/data'

const modelType = ref('remote')
const modelName = ref('qwen-max')

const dataStore = useDataStore()
const {
  status, answer_zh ,answer_en, messages, logs, status_zh
} = storeToRefs(dataStore)

function send(cmd: string){
  console.log('send', cmd)
  if(cmd === 'synthesis') {
    window.electron.ipcRenderer.send(`server.${cmd}`, answer_en.value)
    dataStore.addResponse()
  }
  else if(cmd === 'translate') { 
    window.electron.ipcRenderer.send(
      `server.${cmd}`,
      { type: modelType.value, name: modelName.value, text: answer_zh.value }
    )
  }
  else {
    window.electron.ipcRenderer.send(`server.${cmd}`)
  }
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
  margin: 10px 0;
  scrollbar-width: none;
}

.main-control {
  margin-top: 10px;
  display: flex;
  justify-content: center;
}

.label {
  width: 100px;
  text-align: right;
  margin-right: 10px;
}

button {
  margin-right: 10px;
  min-width: 60px;
}
</style>
