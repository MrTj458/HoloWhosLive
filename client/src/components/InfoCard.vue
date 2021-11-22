<template>
  <a :href="channelUrl">
    <div :class="{ card: true, is_live: props.channel.is_live }">
      <img
        :src="props.channel.image"
        :alt="props.channel.display_name"
      />
      <div class="card-info">
        <h2>{{ props.channel.first_name }} {{ props.channel.last_name }}</h2>
        <p>{{ props.channel.group.name }}</p>
        <small>{{ props.channel.display_name }}</small>
        <small>{{ subCount }}</small>
      </div>
    </div>
  </a>
</template>

<script setup>
import { defineProps, computed } from 'vue'

const props = defineProps(['channel'])

/**
 * Create channel URL based on Youtube ID
 */
const channelUrl = computed(() => {
  if (props.channel.platform === 'Youtube') {
    return `https://youtube.com/channel/${props.channel.channel_id}/live`
  } else {
    return `https://www.twitch.tv/${props.channel.channel_id}`
  }
})

/**
 * Add commas to subcount
 */
const subCount = computed(() => {
  if (props.channel.subscribers) {
    return `${props.channel.subscribers
    .toString()
    .replace(/\B(?=(\d{3})+(?!\d))/g, ',')} Subscribers`
  } else {
    return `${props.channel.view_count
    .toString()
    .replace(/\B(?=(\d{3})+(?!\d))/g, ',')} Views`
  }
})
</script>

<style scoped>
a {
  text-decoration: none;
  justify-self: center;
}

img {
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  width: 100%;
}

.card {
  background-color: var(--highlight);
  box-shadow: 1px 3px 5px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  text-align: center;
  text-decoration: none;
  transition: all 0.1s ease;
  width: 100%;
  max-width: 240px;
  height: 100%;
}

.card:hover {
  transform: scale(1.01);
  box-shadow: 4px 12px 20px rgba(0, 0, 0, 0.1);
  cursor: pointer;
}

.card-info {
  padding: 10px;
}

.is_live {
  border: 4px solid var(--live-color);
}

small {
  display: block;
}

@media only screen and (max-width: 600px) {
  .card {
    width: 48vw;
  }
}
</style>
