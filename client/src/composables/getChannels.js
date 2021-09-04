import { ref } from 'vue'
import api from '../utils/axios'

const getChannels = () => {
  const data = ref(null)
  const error = ref(null)
  const loading = ref(false)

  const getData = async () => {
    error.value = null
    loading.value = true

    try {
      const res = await api.get('/api/channels/')
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
