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
      <div class="flex">
        <!-- <li>
          <ThemeToggle />
        </li> -->
        <li>
          <!-- Filter -->
          Showing:
          <select v-model="filter" class="dropdown">
            <option value="0" selected>All</option>
            <template v-for="group in groups" :key="group.id">
              <option :value="group.id">{{ group.name }}</option>
            </template>
          </select>
        </li>
      </div>
    </ul>
  </nav>
</template>

<script setup>
import useFilter from '@/composables/useFilter'
import getGroups from '@/composables/getGroups'

const { filter } = useFilter()
const { data: groups } = getGroups()
</script>

<style scoped>
a {
  color: var(--text-color);
  text-decoration: none;
}

h1 {
  font-size: 2rem;
}

nav {
  width: 100%;
  background-color: var(--highlight);
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
  background-color: var(--background);
  box-shadow: 1px 3px 5px rgba(0, 0, 0, 0.1);
}

.flex {
  display: flex;
  align-items: center;
}
</style>
