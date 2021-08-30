<template>
  <nav>
    <ul>
      <div>
        <li>
          <router-link :to="{ name: 'Home' }">
            <h1>Holo Who's Live</h1>
          </router-link>
        </li>
      </div>
      <div>
        <li>
          Showing:
          <select @change="changeFilter">
            <option value="All" selected>All</option>
            <option value="English">English</option>
            <option value="Indonesia">Indonesia</option>
            <option value="Japan">Japan</option>
            <option value="Holostars">Holostars</option>
          </select>
        </li>
      </div>
    </ul>
  </nav>
</template>

<script setup>
import useFilter from '@/composables/useFilter'

const { filter } = useFilter()

const changeFilter = (e) => {
  filter.value = e.target.value
}
</script>

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
  justify-content: space-between;
  align-items: center;
}
</style>
