import './App.css';

import axios from 'axios';

import { useEffect, useState } from 'react'
import Cookies from 'js-cookie';

import LoginPrompt from './LoginPrompt.jsx'
import Map from './Map.jsx'
import ServerInfo from './ServerInfo';
import InfoPanel from './InfoPanel';
import { SelectionProvider } from './SelectionProvider';


function getAccessToken() {
  return Cookies.get('access_token')
}

function logout() {
  Cookies.remove('access_token');
}

function sitRepFetch() {
  console.log('fetching SitRep.')

  const token = getAccessToken();
  let req = axios.get("/api/sitrep", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  req.catch(error => {
    if (error.code === "ERR_NETWORK") {
      console.log("Network error - Backend is likely down or can't be reached")
      return
    }

    if (error.response.status === 401) {
      console.log('Unauthorized - either invalid token (tampered) or expired')
      logout()
    } else {
      console.log('error fetching SitRep: ', error) // fuck
    }
  });

  return req
}

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [sitRep, setSitRep] = useState(null);

  useEffect(() => {
    Cookies.get('access_token') ? setIsLoggedIn(true) : setIsLoggedIn(false);

    if (isLoggedIn) {
      sitRepFetch().then((req) => {
        setSitRep(req.data)
      })

      // in dev mode, refresh every 10 seconds.
      setInterval(() => {
        sitRepFetch().then((req) => {
          setSitRep(req.data)
        })
      }, (import.meta.env.DEV ? 10 : 30) * 1000);
    }
  }, [isLoggedIn])

  if (!isLoggedIn) { return <LoginPrompt /> }

  if (sitRep) {
    return <div>
      <SelectionProvider>
        <div className="banner">
          <img className="sdcslogo" src="/sdcs-logo.png"></img>
          <div className="serverName">Strategic DCS</div>
        </div>
        <Map sitRep={sitRep}>
        </Map>
        <ServerInfo
          online_users={sitRep.online_users}
          seconds_left_until_restart={sitRep.seconds_left_until_restart}/>
        <InfoPanel/>
      </SelectionProvider>
    </div>
  } else {
    return <div>
      Loading...
    </div>
  }
}

export default App;
