import { ref } from 'vue'
import axios from 'axios'

const getChannels = () => {
  const data = ref([])
  const error = ref(null)
  const loading = ref(false)

  const getData = async () => {
    error.value = null
    loading.value = true

    try {
      const res = await axios.get('http://localhost:8000/api/channels')
      data.value = res.data
      loading.value = false
    } catch (err) {
      console.error(err.message)
      error.value = err.message
      loading.value = false
      data.value = []
    }
  }
  getData()

  return {
    data,
    error,
    loading,
  }
}

export default getChannels
