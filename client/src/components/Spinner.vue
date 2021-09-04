<template>
  <div class="spinner"></div>
</template>

<style scoped>
.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid var(--text-color);
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-radius: 50%;
  animation: spin 1s infinite ease;
  margin: 20px auto;
}

@keyframes spin {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
