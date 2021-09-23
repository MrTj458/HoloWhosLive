import { ref } from 'vue'

const filter = ref(0)

const useFilter = () => {
  return {
    filter,
  }
}

export default useFilter
