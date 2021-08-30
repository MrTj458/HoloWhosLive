<template>
  <div id="main">
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
import NavBar from '@/components/NavBar'
import Footer from '@/components/Footer'
</script>

<style scoped>
#main {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.content {
  max-width: 1200px;
  margin: 0 auto;
}
</style>
