<template>
  <nav>
    <ul>
      <li>
        <router-link :to="{ name: 'Home' }">
          <h1>Holo Who's Live</h1>
        </router-link>
      </li>
    </ul>
  </nav>
</template>

<script></script>

<style scoped>
a {
  color: #000;
  text-decoration: none;
}

h1 {
  font-size: 2rem;
}

nav {
  width: 100%;
  background-color: white;
  padding: 10px;
}

nav ul {
  list-style: none;
  display: flex;
}
</style>
