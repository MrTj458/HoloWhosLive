<template>
  <div class="home">
    <div v-if="!loading">
      <div class="section">
        <ChannelList :channels="liveChannels" />
      </div>
      <hr />
      <div class="section">
        <ChannelList :channels="offlineChannels" />
      </div>
    </div>
    <div v-else><Spinner /></div>
  </div>
</template>

<script setup>
import getChannels from '@/composables/getChannels'
import ChannelList from '@/components/ChannelList'
import Spinner from '@/components/Spinner'
import { computed } from '@vue/reactivity'

const { data: channels, loading } = getChannels()

const sortBySubCount = (channels) => {
  return channels.sort((a, b) => b.subscribers - a.subscribers)
}

const liveChannels = computed(() => {
  return sortBySubCount(channels.value.filter((c) => c.is_live))
})

const offlineChannels = computed(() => {
  return sortBySubCount(channels.value.filter((c) => !c.is_live))
})
</script>

<style scoped>
.home {
  margin: 30px auto;
  max-width: 1200px;
}

.section {
  color: red;
  text-align: center;
  margin: 20px;
}
</style>
