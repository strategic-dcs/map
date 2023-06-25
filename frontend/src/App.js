import './App.css';

import { MapContainer, TileLayer, Marker, Polygon } from 'react-leaflet'
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

      let gridPolygons = [];

      for (let zone of sitRep.grid.zones) {
        let lineStyle = zone.state.line_style.toLowerCase()

        let line_color = [
          zone.state.line_color[0],
          zone.state.line_color[1],
          zone.state.line_color[2],
          zone.state.line_color[3],
        ]

        line_color[0] = line_color[0] * 210;
        line_color[1] = line_color[1] * 210;
        line_color[2] = line_color[2] * 210;
        line_color[3] = line_color[3] * 255;

        let fill_color = [
          zone.state.fill_color[0],
          zone.state.fill_color[1],
          zone.state.fill_color[2],
          zone.state.fill_color[3],
        ]

        fill_color[0] = fill_color[0] * 255;
        fill_color[1] = fill_color[1] * 255;
        fill_color[2] = fill_color[2] * 255;
        fill_color[3] = fill_color[3] * 5;

        let options = {
          color: `rgba(${line_color})`,
          fillColor: `rgba(${fill_color})`,
          weight: 1,
          dashArray: lineStyle === 'dashed' ? '5, 5' : null
        }

        let pos = [
          [zone.points[0].lat, zone.points[0].lon],
          [zone.points[1].lat, zone.points[1].lon],
          [zone.points[2].lat, zone.points[2].lon],
        ]
        // TODO: replace random with correct key
        gridPolygons.push(<Polygon key={Math.random()} pathOptions={options} positions={pos}/>);
      }

      return <div>
        <MapContainer id="map" center={sitRep.theater_center}
              zoom={7.8}
              // maxZoom={12}
              // minZoom={7.5}

              zoomDelta={0.25}
              zoomSnap={0}
              wheelPxPerZoomLevel={220}>
          <TileLayer
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            // accessToken="pk.eyJ1IjoiY2Vsc29kYW50YXMiLCJhIjoiY2tnNWk4ZWlpMGcyZzJ5bDdjZTU5c2IwdCJ9.1dK2LqeGzVzILLxUToadzg"
            accessToken="pk.eyJ1IjoiY2Vsc29kYW50YXMiLCJhIjoiY2tnNWk4ZWlpMGcyZzJ5bDdjZTU5c2IwdCJ9.1dK2LqeGzVzILLxUToadzg"
            // id={'celsodantas/cljb9vfy5002i01nr1vxkffwl'}
            // id={'celsodantas/cljb9vfy5002i01nr1vxkffwl/draft'}
            id={"celsodantas/cljbgm8oe008h01o049ln1xht/draft"}
            // default light
            //url='https://api.mapbox.com/styles/v1/mapbox/streets-v12/tiles/{z}/{x}/{y}?access_token={accessToken}'
            url='https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}'
          />


          {gridPolygons}
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
