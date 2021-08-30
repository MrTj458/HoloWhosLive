<template>
  <div class="home">
    <div v-if="!loading">
      <!-- Live Channels -->
      <div>
        <ChannelList :channels="liveChannels" />
      </div>

      <hr v-if="liveChannels.length" />

      <!-- Offline Channels -->
      <div>
        <ChannelList :channels="offlineChannels" />
      </div>
    </div>
    <div v-else><Spinner /></div>
  </div>
</template>

<script setup>
import { computed } from '@vue/reactivity'

import useFilter from '@/composables/useFilter'
import getChannels from '@/composables/getChannels'

import ChannelList from '@/components/ChannelList'
import Spinner from '@/components/Spinner'

const { filter } = useFilter()
const { data: channels, loading } = getChannels()

const sortBySubCount = (channels) => {
  return channels.sort((a, b) => b.subscribers - a.subscribers)
}

const filteredChannels = computed(() => {
  if (filter.value === 'All') {
    return channels.value
  }
  return channels.value.filter((c) => c.group === filter.value)
})

const liveChannels = computed(() => {
  return sortBySubCount(filteredChannels.value.filter((c) => c.is_live))
})

const offlineChannels = computed(() => {
  return sortBySubCount(filteredChannels.value.filter((c) => !c.is_live))
})
</script>

<style></style>
