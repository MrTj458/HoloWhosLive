import { useContext } from 'react'
import styled from 'styled-components'
import ChannelList from '../components/ChannelList'
import Spinner from '../components/Spinner'
import { YoutubeContext } from '../context/ChannelContext'

const HomeContainer = styled.div`
  text-align: center;

  h1 {
    text-align: center;
    margin-bottom: 2rem;
    margin-top: 1rem;
  }

  h3 {
    margin: 1rem 0;
  }
`

export default function Home() {
  const ytData = useContext(YoutubeContext)

  return (
    <HomeContainer>
      <h1>Holo Who's live</h1>

      {ytData.length > 0 ? <ChannelList channels={ytData} /> : <Spinner />}
    </HomeContainer>
  )
}
