<template>
  <div class="footer">
    <div>
      <ThemeToggle />
    </div>
    <div>
      Created by
      <a href="https://twitter.com/tjhod" target="_blank">@tjhod</a>
      |
      <a href="https://www.trevorhodsdon.dev/" target="_blank"
        >trevorhodsdon.dev</a
      >
    </div>
  </div>
</template>

<script setup>
import ThemeToggle from '@/components/ThemeToggle'
</script>

<style scoped>
.footer {
  background-color: var(--highlight);
  padding: 5px 20px;
  text-align: right;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>
