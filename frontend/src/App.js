import './App.css';

import { MapContainer } from 'react-leaflet/MapContainer'
import { TileLayer } from 'react-leaflet/TileLayer'
import { useMap } from 'react-leaflet/hooks'

let sitRep = {
  theater: {
    centre: [43.05, 39.40] // caucassus
  }
}

function getSitrep() {
  return sitRep;
}

function App() {
  let sitrep = getSitrep();

  return (
    <MapContainer center={sitrep.theater.centre} 
          zoom={7}
          maxZoom={12} 
          minZoom={7.5} 
          
          zoomDelta={0.25}
          zoomSnap={0}
          wheelPxPerZoomLevel={220}
          scrollWheelZoom={false}>
      <TileLayer
      attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      // url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      accessToken="pk.eyJ1IjoiY2Vsc29kYW50YXMiLCJhIjoiY2tnNWk4ZWlpMGcyZzJ5bDdjZTU5c2IwdCJ9.1dK2LqeGzVzILLxUToadzg"
      id={'celsodantas/ckgxw7aad1m1519msfaop1316'} 
      url='https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}'
      /> 

    </MapContainer>
  );
}

export default App;
