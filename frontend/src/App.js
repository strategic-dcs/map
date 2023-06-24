import './App.css';

import { MapContainer, TileLayer, Marker } from 'react-leaflet'
import L from 'leaflet'
import axios from 'axios';

import React, { useEffect, useState } from 'react'
import Cookies from 'js-cookie';

// move this to its own component
import './login.css';

function isLoggedIn() {
  Cookies.get('access_token')
}

function getAccessToken() {
  return Cookies.get('access_token')
}

// clear the access token cookie
function logout() {
  Cookies.remove('access_token');
}

// async function that fetches the sitrep from the backend
async function sitRepFetch(setSitRep, setIsSitRepLoaded, setIsLoggedIn) {
  console.log('fetching SitRep')

  if (isLoggedIn() === false) {
    return
  }

  const token = getAccessToken();
  const response = await axios.get('http://localhost:8000/api/sitrep', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (response.status === 401) {
    console.log('unauthorized')
    logout();
    setIsLoggedIn(false)
  } else {
    console.log(response.data)
    setSitRep(response.data);
    setIsSitRepLoaded(true);
  }
}

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isSitRepLoaded, setIsSitRepLoaded] = useState(false);
  const [sitRep, setSitRep] = useState({});

  useEffect(() => {
    Cookies.get('access_token') ? setIsLoggedIn(true) : setIsLoggedIn(false);

    if (isLoggedIn) {
      sitRepFetch(setSitRep, setIsSitRepLoaded, setIsLoggedIn)
    }
  }, [isLoggedIn, setSitRep, setIsSitRepLoaded])


  // todo: move this to its own component
  const loginPrompt = <div className="lightbox-container">
      <div className="lightbox">
        <a href="https://discord.com/api/oauth2/authorize?client_id=1121891789096374382&redirect_uri=http://localhost:3000/auth/callback&scope=identify%20guilds%20guilds.members.read&response_type=code" className="login-link">
          Please Login on Discord
        </a>
      </div>
    </div>

  if (isLoggedIn) {
    if (isSitRepLoaded) {
      let airportsMarkers = []

    for(let airfield of sitRep.airfields) {
      let iconHtml = `
          <div class="airportMarker">
              <img class="icon" src="assets/images/airport-circle.svg">
              <div class="name">${airfield.name}</div>
          </div>
      `
      let icon = new L.DivIcon({className: 'airportIcon', html: iconHtml})
      airportsMarkers.push(<Marker key={airfield.name} position={airfield.position} icon={icon}></Marker>)
    }
      return <div>
        <MapContainer center={sitRep.theater_center}
              zoom={7}
              maxZoom={12}
              minZoom={7.5}

              zoomDelta={0.25}
              zoomSnap={0}
              wheelPxPerZoomLevel={220}>
          <TileLayer
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            accessToken="pk.eyJ1IjoiY2Vsc29kYW50YXMiLCJhIjoiY2tnNWk4ZWlpMGcyZzJ5bDdjZTU5c2IwdCJ9.1dK2LqeGzVzILLxUToadzg"
            id={'celsodantas/ckgxw7aad1m1519msfaop1316'}
            url='https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}'
          />

          {airportsMarkers}

        </MapContainer>
      </div>
    } else {
      return <div>
        loading...
      </div>
    }

  } else {
    return <div>
      {loginPrompt}
    </div>
  }
}

export default App;
