<template>
  <div class="home">
    <div v-if="error" class="center">
      <h2>Error connecting to server! Please try again later.</h2>
    </div>
    <div v-else>
      <div v-if="loading">
        <Spinner />
      </div>
      <div v-else>
        <!-- Live Channels -->
        <transition name="live" mode="out-in">
          <div v-if="liveChannels.length > 0">
            <ChannelList :channels="liveChannels" />
          </div>
          <div v-else class="center">
            <h2>No one is live right now 🙁</h2>
          </div>
        </transition>

        <!-- Offline Channels -->
        <div>
          <ChannelList :channels="offlineChannels" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from '@vue/reactivity'

import useFilter from '@/composables/useFilter'
import getChannels from '@/composables/getChannels'

import ChannelList from '@/components/ChannelList'
import Spinner from '@/components/Spinner'

const { filter } = useFilter()
const { data: channels, loading, error } = getChannels()

const sortBySubCount = (channels) => {
  return channels.sort((a, b) => b.subscribers - a.subscribers)
}

/**
 * Filter channels based on the selected filter
 */
const filteredChannels = computed(() => {
  if (filter.value === 'All') {
    return channels.value
  }
  return channels.value.filter((c) => c.group === filter.value)
})

/**
 * Live channels based on selected filter
 */
const liveChannels = computed(() => {
  return sortBySubCount(filteredChannels.value.filter((c) => c.is_live))
})

/**
 * Offline channels based on selected filter
 */
const offlineChannels = computed(() => {
  return sortBySubCount(filteredChannels.value.filter((c) => !c.is_live))
})
</script>

<style scoped>
.center {
  margin-top: 30px;
  text-align: center;
}

.live-enter-from,
.live-leave-to {
  opacity: 0;
  transform: scale(0.5);
}

.live-enter-active {
  transition: all 0.3s ease;
}
</style>
