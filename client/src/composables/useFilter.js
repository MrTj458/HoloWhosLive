import { ref } from 'vue'

const filter = ref('All')

const useFilter = () => {
  return {
    filter,
  }
}

export default useFilter
