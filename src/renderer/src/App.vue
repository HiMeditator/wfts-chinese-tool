<template>
  <div class="window">
    <TitleBar />
    <Comm />
    <AllLogs />
  </div>
</template>

<script setup lang="ts">
import TitleBar from './components/TitleBar.vue';
import Comm from './components/Comm.vue'
import AllLogs from './components/AllLogs.vue';
</script>

<style scoped>
.window {
  width: 100%;
  height: 100vh;
  background-color: rgba(227, 232, 248, 0.8);
  display: flex;
  flex-direction: column;
}
</style>
