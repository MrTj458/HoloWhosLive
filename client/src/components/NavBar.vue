<template>
  <nav>
    <ul>
      <!-- Left side -->
      <div>
        <li>
          <router-link :to="{ name: 'Home' }">
            <h1>Holo Who's Live</h1>
          </router-link>
        </li>
      </div>

      <!-- Right Side -->
      <div>
        <li>
          <!-- Filter -->
          Showing:
          <select v-model="filter" class="dropdown">
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

/* Dropdown */
.dropdown {
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 10px 20px;
  background-color: #eee;
  box-shadow: 1px 3px 5px rgba(0, 0, 0, 0.1);
}
</style>
