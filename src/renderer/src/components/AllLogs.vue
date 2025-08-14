<template>
  <div class="all-logs">
    <div class="nav-bar">
      <a-menu
        v-model:selectedKeys="current"
        mode="horizontal" :items="items"
        class="bg-color"
      />
    </div>
    <a-list
      size="small" class="bg-color logs"
      :data-source="logs"
      v-if="current[0] === 'logs'"
    >
      <template #renderItem="{ item }">
          <a-list-item :class="[item.type]">
            {{ item.content }}
          </a-list-item>
      </template>
    </a-list>
    <div class="bg-color messages" v-else>
      <a-empty
        v-if="messages.length === 0"
        :image="simpleImage"
        style="padding: 16px 0 2px;"
      />
      <div v-for="(msg, idx) in messages" :key="idx" :class="[msg.role]">
        <div>{{ msg.content }}</div>
        <div class="translation">{{ msg.translation }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, h } from 'vue'
import { storeToRefs } from 'pinia';
import { useDataStore } from '@renderer/stores/data'
import { MailOutlined, AppstoreOutlined } from '@ant-design/icons-vue';
import { MenuProps } from 'ant-design-vue';
import { Empty } from 'ant-design-vue';
const simpleImage = Empty.PRESENTED_IMAGE_SIMPLE;
const items = ref<MenuProps['items']>([
    {
    key: 'messages',
    icon: () => h(MailOutlined),
    label: '聊天',
  },
  {
    key: 'logs',
    icon: () => h(AppstoreOutlined),
    label: '日志',
  }
])
const dataStore = useDataStore()
const { logs, messages } = storeToRefs(dataStore)

const current = ref<string[]>(['messages']);
</script>

<style scoped>
.all-logs {
  margin: 12px;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  scrollbar-width: none;
}

.nav-bar {
  position: sticky;
  top: 0;
  z-index: 10;
}

.bg-color {
  background-color: #fff9;
}

.logs {
  padding-top: 10px;
}

.info, .warn, .error {
  padding: 2px;
  font-size: 12px;
  padding: 8px 10px;
  line-height: 1.6em;
}

.info:hover, .warn:hover, .error:hover {
  background-color: #aaa2;
}

.warn {
  color: #faad14;
}

.error {
  color: #ff4d4f;
}

.messages {
  padding: 10px;
  display: flex;
  flex-direction: column;
}

.translation {
  display: block;
  border-left: 3px solid #69b1ff;
  padding-left: 4px;
}

.Stella, .You {
  margin: 5px;
  padding: 6px 12px;
  border-radius: 8px;
  max-width: 80%;
  min-width: 40%;
  line-height: 1.6em;
}

.Stella {
  background: rgba(0, 0, 128, 0.05);
  align-self: flex-start;
}

.Stella:hover {
  background: rgba(0, 0, 128, 0.08);
}

.You {
  background: rgba(0, 128, 0, 0.05);
  align-self: flex-end;
}

.You:hover {
  background: rgba(0, 128, 0, 0.08);
}
</style>
