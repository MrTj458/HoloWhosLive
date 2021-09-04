<template>
  <div id="main" :class="theme">
    <div>
      <NavBar />
      <div class="content">
        <router-view />
      </div>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import useTheme from '@/composables/useTheme'

import NavBar from '@/components/NavBar'
import Footer from '@/components/Footer'

const { theme } = useTheme()
</script>

<style scoped>
#main {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: var(--background);
  font-family: 'Nunito', sans-serif;
}

.content {
  max-width: 1200px;
  margin: 0 auto;
}
</style>
