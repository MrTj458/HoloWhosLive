import styled from 'styled-components'
import ChannelCard from '../components/ChannelCard'

const ChannelListStyles = styled.div`
  h2 {
    margin-bottom: 0.5rem;
  }

  hr {
    max-width: 1200px;
    margin-bottom: 1rem;
  }
`

const ChannelContainer = styled.div`
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
`

export default function ChannelList({ channels }) {
  const liveChannels = channels.filter((channel) => channel.is_live)
  const offlineChannels = channels.filter((channel) => !channel.is_live)

  return (
    <ChannelListStyles>
      {liveChannels.length !== 0 && (
        <>
          <h2>Live</h2>
          <ChannelContainer>
            {liveChannels.map((channel) => (
              <ChannelCard key={channel.id} channel={channel} />
            ))}
          </ChannelContainer>
        </>
      )}

      {offlineChannels.length !== 0 && (
        <>
          <h2>Offline</h2>
          <ChannelContainer>
            {offlineChannels.map((channel) => (
              <ChannelCard key={channel.id} channel={channel} />
            ))}
          </ChannelContainer>
        </>
      )}
    </ChannelListStyles>
  )
}
