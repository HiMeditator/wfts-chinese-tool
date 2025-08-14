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
    <a-row>
      <a-col :span="12">
        <a-textarea
          ref="textarea1"
          class="prompt-input"
          v-model:value="input"
          placeholder="输入中文回答"
          @input="syncHeight"
          :auto-size="{ minRows: 3, maxRows: 10 }"
        />
      </a-col>
      <a-col :span="12">
        <a-textarea
          ref="textarea2"
          class="prompt-input"
          v-model:value="translation"
          placeholder="英文翻译"
          @input="syncHeight"
          :auto-size="{ minRows: 3, maxRows: 10 }"
        />
      </a-col>
    </a-row>
    <div class="main-control">
      <template v-if="command === 'Stopped'">
        <a-button size="small" type="primary" @click="send('start')">启动</a-button>
      </template>
      <template v-else>
        <a-button size="small" danger ghost @click="send('stop')">停止</a-button>
      </template>
      <a-button
        size="small" type="primary" @click="send('listen')"
        :disabled="status === 'stopped'"
      >语音监听</a-button>
      <a-button
        size="small" type="primary" @click="send('')"
        :disabled="status === 'stopped'"
      >语音输入</a-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { storeToRefs } from 'pinia';
import { useDataStore } from '@renderer/stores/data'

/*
《Whispers from the Star》是一款科幻主题互动游戏。背景设定在太空，玩家需要通过文本、语音等形式与受困星球的游戏角色 Stella 实时互动，核心目标是协助她成功撤离险境，完成通关。

作为玩家，你需全程代入居住在地球上的工程师 Chen 的身份，回答要求如下：
- 不要在回答开头添加任何与互动无关的表述（如身份说明、思考过程等）
- 基于工程师的专业视角回应 Stella 的提问
- 结合太空探索常识与工程思维，为她提供切实可行的解决方案
- 保持沟通的及时性与逻辑性，推动剧情进展
- 输出内容保证简洁易懂
- 单次回答不要输出过多内容
*/

const input = ref('')
const translation = ref('')

const textarea1 = ref<HTMLTextAreaElement>()
const textarea2 = ref<HTMLTextAreaElement>()

const dataStore = useDataStore()
const { status, messages, logs, command } = storeToRefs(dataStore)

function syncHeight() {
  nextTick(() => {
    if (textarea1.value && textarea2.value) {
      const height1 = textarea1.value.scrollHeight
      const height2 = textarea2.value.scrollHeight
      const maxHeight = Math.max(height1, height2)
      
      if (height1 !== maxHeight) {
        textarea1.value.style.height = `${maxHeight}px`
      }
      if (height2 !== maxHeight) {
        textarea2.value.style.height = `${maxHeight}px`
      }
    }
  })
}

function send(cmd: string){
  if(cmd === '') { cmd = command.value.toLowerCase() }
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
  margin: 10px 0;
}

.main-control {
  margin-top: 10px;
  display: flex;
  justify-content: center;
}

button {
  margin-right: 10px;
  min-width: 60px;
}
</style>
