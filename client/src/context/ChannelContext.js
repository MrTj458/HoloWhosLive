import { createContext, useEffect, useState } from 'react'
import axios from 'axios'

export const YoutubeContext = createContext()

export default function ChannelContext({ children }) {
  const [channelData, setChannelData] = useState([])

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    const res = await axios.get('/api/youtube')
    setChannelData(res.data)
  }

  return (
    <>
      <YoutubeContext.Provider value={channelData}>
        {children}
      </YoutubeContext.Provider>
    </>
  )
}
