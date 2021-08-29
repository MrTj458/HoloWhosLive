<template>
  <a :href="channelUrl">
    <div :class="{ card: true, is_live: props.channel.is_live }">
      <img :src="props.channel.images.medium" alt="" />
      <div class="card-info">
        <!-- <h2 v-if="props.channel.is_live" class="live-text">Live Now!</h2> -->
        <h3 class="card-title">
          {{ props.channel.first_name }} {{ props.channel.last_name }}
        </h3>
        <p>{{ subCount }} subscribers</p>
      </div>
    </div>
  </a>
</template>

<script setup>
import { defineProps, computed } from 'vue'

const props = defineProps(['channel'])

const channelUrl = computed(() => {
  return `https://youtube.com/channel/${props.channel.channel_id}/live`
})

const subCount = computed(() => {
  return props.channel.subscribers
    .toString()
    .replace(/\B(?=(\d{3})+(?!\d))/g, ',')
})
</script>

<style scoped>
a {
  text-decoration: none;
}

img {
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.card {
  background-color: white;
  box-shadow: 1px 3px 5px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  text-align: center;
  text-decoration: none;
  color: #000;
  transition: all 0.1s ease;
}

.card:hover {
  transform: scale(1.01);
  box-shadow: 4px 12px 20px rgba(0, 0, 0, 0.1);
  cursor: pointer;
}

.card-title {
  margin-bottom: 10px;
}

.card-info {
  padding-top: 10px;
  padding-bottom: 15px;
}

.is_live {
  border: 4px solid red;
}

.live-text {
  color: red;
  margin-bottom: 5px;
}
</style>
