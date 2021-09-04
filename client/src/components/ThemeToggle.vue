<template>
  <div>
    <input
      v-model="theme"
      @change="saveTheme"
      type="checkbox"
      value="dark"
      id="toggle"
    />
    <label v-if="theme.length === 1" for="toggle">
      <span class="material-icons-outlined">
        light_mode
      </span>
    </label>
    <label v-else for="toggle">
      <span class="material-icons-outlined">
        dark_mode
      </span>
    </label>
  </div>
</template>

<script setup>
import useTheme from '@/composables/useTheme'
import { onMounted } from '@vue/runtime-core'

const { theme } = useTheme()

onMounted(() => {
  const storedTheme = localStorage.getItem('dark')

  if (storedTheme) {
    theme.value = ['dark']
  }
})

const saveTheme = () => {
  if (theme.value.length === 1) {
    localStorage.setItem('dark', true)
  } else {
    localStorage.removeItem('dark')
  }
}
</script>

<style scoped>
input {
  display: none;
}

label:hover {
  cursor: pointer;
}
</style>
