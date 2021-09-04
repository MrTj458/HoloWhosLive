import axios from 'axios'

const api = axios.create({
  baseURL:
    process.env.NODE_ENV === 'development'
      ? 'http://localhost:8000'
      : 'https://api.holowhos.live/',
})

export default api
