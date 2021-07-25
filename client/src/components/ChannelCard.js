import { Link } from 'wouter'
import styled from 'styled-components'

const Card = styled.div`
  padding: 0.5rem;
  border-radius: 4px;
  width: 260px;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #5c1469;
  color: #fff;

  border: ${(props) => (props.live ? '4px solid red' : 'none')};

  img {
    border-radius: 4px;
  }

  h3 {
    margin-top: 0.7rem;
    text-align: center;
    font-weight: bold;
    cursor: pointer;

    &:hover {
      text-decoration: underline;
    }
  }

  p {
    margin-top: 0.4rem;
  }

  a {
    margin-top: 1rem;
    border: 1px solid #fff;
    border-radius: 4px;
    padding: 0.5rem 1rem;
    color: #fff;
    text-decoration: none;

    &:hover {
      color: #a625be;
      background: #fff;
    }
  }
`

export default function ChannelCard({ channel }) {
  const liveVideo = channel.videos.find(
    (video) => video.live_broadcast_content === 'live'
  )

  return (
    <Card live={channel.is_live}>
      <img src={channel.thumbnails.medium.url} alt={channel.channel_name} />
      <Link to={`/${channel.channel_id}`}>
        <h3>
          {channel.first_name} {channel.last_name}
        </h3>
      </Link>
      <p>
        {channel.statistics.subscriberCount.replace(
          /\B(?=(\d{3})+(?!\d))/g,
          ','
        )}{' '}
        subscribers
      </p>
      <p>{channel.statistics.videoCount} videos</p>
      {liveVideo ? (
        <a href={`https://www.youtube.com/watch?v=${liveVideo.id}`}>
          Go To Stream
        </a>
      ) : (
        <a href={`https://www.youtube.com/channel/${channel.channel_id}`}>
          Go To Channel
        </a>
      )}
    </Card>
  )
}
