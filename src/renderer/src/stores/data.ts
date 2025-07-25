import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { Status, ConsoleLog, Message } from '@renderer/types'

export const useDataStore = defineStore('data', () => {
  const status = ref<Status>('stopped')
  const messages = ref<Message[]>([])
  const logs = ref<ConsoleLog[]>([])

  const command = computed(() => {
    switch(status.value){
      case 'stopped': return 'Stopped';
      case 'connected': case 'ready': return 'Listen';
      case 'listening': return 'Answer';
      case 'answering': case 'synthesising': return 'Pending';
      case 'sythesized': return 'Output';
      case 'outputting': return 'Pending';
    }
  })

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
    if(msg.command === 'ready') status.value = 'connected'
    else if(msg.command === 'status') status.value = msg.content
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
    else if(msg.command === 'answer') {
      messages.value.push({
        role: 'You',
        content: msg['content'],
        translation: "",
        end: true
      })
    }
  })

  return {
    status,
    messages,
    logs,
    command,
  }
})
