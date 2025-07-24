<template>
  <div class="window">
    <TitleBar />
    <Comm />
  </div>
</template>

<script setup lang="ts">
import TitleBar from './components/TitleBar.vue';
import Comm from './components/Comm.vue'
</script>

<style scoped>
.window {
  width: 100%;
  height: 100vh;
  background-color: rgba(227, 232, 241, 0.75);
  border-radius: 10px;
}
</style>
