import { ref } from 'vue'

const theme = ref(localStorage.getItem('dark') ? ['dark'] : [])

const useTheme = () => {
  return {
    theme,
  }
}

export default useTheme
