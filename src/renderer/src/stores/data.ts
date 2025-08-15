import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { Status, ConsoleLog, Message } from '@renderer/types'

export const useDataStore = defineStore('data', () => {
  const status = ref<Status>('stopped')
  let answer_en_pre = ""
  let answer_zh_pre = ""
  const answer_en = ref<string>('')
  const answer_zh = ref<string>('')
  const messages = ref<Message[]>([])
  const logs = ref<ConsoleLog[]>([])
  const immSynthesis = ref(false)

  const status_zh = computed(() => {
    switch(status.value){
      case 'stopped': return '未连接';
      case 'connecting': return '正在连接';
      case 'ready': return '准备就绪';
      case 'translating': return '翻译中';
      case 'listening': return '语音监听';
      case 'recording': return '语音输入';
      case 'synthesising': return '语音合成';
      case 'outputting': return '输出音频';
    }
  })

  function resetAnswer() {
    answer_en_pre = ""
    answer_zh_pre = ""
    answer_en.value = ""
    answer_zh.value = ""
  }

  function addResponse() {
    messages.value.push({
      role: "You",
      content: answer_en.value,
      translation: answer_zh.value,
      end: true
    })
  }

  window.electron.ipcRenderer.on('info.send', (_, msg: string) => {
    logs.value.push({type: 'info', content: msg})
  })

  window.electron.ipcRenderer.on('warn.send', (_, msg: string) => {
    logs.value.push({type: 'warn', content: msg})
  })

  window.electron.ipcRenderer.on('error.send', (_, msg: string) => {
    logs.value.push({type: 'error', content: msg})
  })

  window.electron.ipcRenderer.on('message.send', (_, msg: any) => {
    console.log(msg)
    if(msg.command === 'ready') status.value = 'connecting'
    else if(msg.command === 'status'){
      status.value = msg.content
      if(msg.content === 'recording') { resetAnswer() }
    }
    else if(msg.command === 'caption') {
      if(messages.value.length && !messages.value[messages.value.length - 1].end) {
        messages.value.pop()
      }
      messages.value.push({
        role: 'Stella',
        content: msg['text'],
        translation: msg['translation'],
        end: msg['end']
      })
    }
    else if(msg.command === 'record') {
      if(msg.index === -1) {
        answer_en.value = msg.translation,
        answer_zh.value = msg.text
        answer_en_pre = ""
        answer_zh_pre = ""
        if(immSynthesis.value) {
          window.electron.ipcRenderer.send(`server.synthesis`, answer_en.value)
          addResponse()
        }
        return
      }
      answer_en.value = answer_en_pre + msg.translation
      answer_zh.value = answer_zh_pre + msg.text
      if(msg.end) {
        answer_en_pre = answer_en.value
        answer_zh_pre = answer_zh.value
      }
    }
  })

  return {
    status,
    status_zh,
    answer_en,
    answer_zh,
    messages,
    logs,
    immSynthesis,
    addResponse,
  }
})
