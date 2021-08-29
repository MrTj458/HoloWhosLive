<template>
  <div class="list">
    <transition-group name="channels" appear>
      <div v-for="channel in props.channels" :key="channel.id">
        <InfoCard :channel="channel" />
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

import InfoCard from '@/components/InfoCard'

const props = defineProps(['channels'])
</script>

<style scoped>
.list {
  margin: 0 auto;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 20px;
}

.channels-enter-from {
  opacity: 0;
  transform: scale(0.5);
}

.channels-enter-active {
  transition: all 0.3s ease;
}
</style>
