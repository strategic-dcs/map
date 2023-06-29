import { MapContainer, TileLayer, Marker, Polygon,  } from 'react-leaflet'
import L from 'leaflet'
import airportIcon from '/airport-circle.svg'

function Map(props) {

  let airportsMarkers = []
  let sitRep = props.sitRep

  for(let airfield of sitRep.airfields) {
    let iconHtml = `
      <div class="airportMarker">
          <img class="icon" src="${airportIcon}">
          <div class="name">${airfield.name}</div>
      </div>
      `
    let icon = new L.DivIcon({className: 'airportIcon', html: iconHtml})
    airportsMarkers.push(<Marker key={airfield.name} position={airfield.position} icon={icon}></Marker>)
  }

  let gridPolygons = []

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

  return <MapContainer id="map" center={sitRep.theater_center}
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

}

export default Map;
