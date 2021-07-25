import styled from 'styled-components'
import { Link } from 'wouter'

const NavStyles = styled.div`
  background-color: #5c1469;
  padding: 1rem 2rem;
  margin-bottom: 2rem;

  h1 {
    cursor: pointer;
  }
`

export default function NavBar() {
  return (
    <NavStyles>
      <nav>
        <Link to="/">
          <h1>Holo Who's Live</h1>
        </Link>
      </nav>
    </NavStyles>
  )
}
