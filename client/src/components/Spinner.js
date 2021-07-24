import styled, { keyframes } from 'styled-components'

const rotate = keyframes`
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
`

const Spinner = styled.div`
  width: 50px;
  height: 50px;
  border: 10px solid #5c1469;
  border-top-color: transparent;
  border-radius: 50%;
  animation: ${rotate} 0.5s linear infinite;
  margin: 0 auto;
`

export default Spinner
