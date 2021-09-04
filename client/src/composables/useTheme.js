import { ref } from 'vue'

const theme = ref([])

const useTheme = () => {
  return {
    theme,
  }
}

export default useTheme
