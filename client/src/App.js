import { Switch, Route } from 'wouter'
import NavBar from './components/NavBar'
import ChannelContext from './context/ChannelContext'
import Channel from './pages/Channel'
import Home from './pages/Home'
import NotFound from './pages/NotFound'

function App() {
  return (
    <ChannelContext>
      <NavBar />
      <Switch>
        <Route path="/" component={Home} />
        <Route path="/:channel_id" component={Channel} />
        <Route component={NotFound} />
      </Switch>
    </ChannelContext>
  )
}

export default App
