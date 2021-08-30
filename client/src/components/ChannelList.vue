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
  margin: 20px auto;
  margin-bottom: 60px;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 20px;
  position: relative;
}

.channels-enter-from,
.channels-leave-to {
  opacity: 0;
  transform: scale(0.5);
}

.channels-enter-active,
.channels-move {
  transition: all 0.3s ease;
}

.channels-leave-active {
  position: absolute;
  transition: all 0.3s ease;
}
</style>
