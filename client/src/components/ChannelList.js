import styled from 'styled-components'
import ChannelCard from '../components/ChannelCard'

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
    <>
      <h3>Live</h3>
      {liveChannels.length === 0 ? (
        <p>No one is live right now 🙁</p>
      ) : (
        <ChannelContainer>
          {liveChannels.map((channel) => (
            <ChannelCard key={channel.id} channel={channel} />
          ))}
        </ChannelContainer>
      )}

      <h3>Offline</h3>
      {offlineChannels.length === 0 ? (
        <p>Everyone is live!</p>
      ) : (
        <ChannelContainer>
          {offlineChannels.map((channel) => (
            <ChannelCard key={channel.id} channel={channel} />
          ))}
        </ChannelContainer>
      )}
    </>
  )
}
