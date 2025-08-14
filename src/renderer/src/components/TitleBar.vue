<template>
  <div class="title-bar">
    <div class="drag-area">
      <img src="../assets/icon.svg" class="logo" >
      <span class="title">Whispers from the Star AI Chat</span>
    </div>
    <div class="option-item" @click="pin">
      <PushpinFilled v-if="pinned" />
      <PushpinOutlined v-else />
    </div>
    <div class="option-item" @click="close">
      <CloseOutlined />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import {
  PushpinOutlined, PushpinFilled, CloseOutlined
} from '@ant-design/icons-vue';

const pinned = ref(true);

function pin() {
  pinned.value = !pinned.value
  window.electron.ipcRenderer.send('window.pin', pinned.value)
}

function close() {
  window.electron.ipcRenderer.send('window.close')
}
</script>

<style scoped>
.title-bar {
  display: flex;
  align-items: center;
  font-size: 14px;
  background-color: rgba(227, 232, 241, 0.9);
}

.drag-area {
  padding: 5px;
  flex-grow: 1;
  -webkit-app-region: drag;
}

.logo {
  height: calc(1em + 10px);
  width: calc(1em + 10px);
}

.title {
  vertical-align: middle;
  vertical-align: center;
  margin-left: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.option-item {
  display: inline-block;
  padding: 9px 12px;
  cursor: pointer;
}

.option-item:hover {
  background-color: #2221;
}
</style>
