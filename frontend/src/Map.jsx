import './Map.css';

import { MapContainer, TileLayer, Marker, Polygon, Popup, AttributionControl } from 'react-leaflet'
import { useMapEvents } from 'react-leaflet/hooks'
import blueAirportIcon from '/blue-airfield.svg'
import redAirportIcon from '/red-airfield.svg'
import neutralAirportIcon from '/neutral-airfield.svg'
import { useSelectionContext } from './SelectionProvider';

const theatres = {
  caucasus: {
    centre: [43.529, 39.449],
    bounds: [[47.953,33.190], [39.522,50.256]],
  },
  syria: {
    centre: [34.058, 35.101],
    bounds: [[38.341, 30.157], [28.141, 42.100]],
  }
}

function MapComponents(props) {
  let markers = []
  let sitRep = props.sitRep

  const { selection, setSelection } = useSelectionContext()

  function handleAirfieldClick(airfield, type='airfield') {
    setSelection({ value: airfield, type: type })
  }

  const map = useMapEvents({
    'click': () => {
      setSelection({}) // clear selection on map click
    },
    'mouseup': () => {
      // Update the URL hash with the current map center
      // that way, on page reload, we can restore the map to the same position
      location.hash = map.getCenter().lat.toFixed(3) + "/" + map.getCenter().lng.toFixed(3)
    }
  })

  for(let airfield of sitRep.airfields_friendly) {
    // Some airfields have a dash in their name, we only want the first part
    // ex. Sochi-Adler -> Sochi - Too long of a name makes the UI ugly.
    const airfield_name = airfield.name.match(/^[^-]+/)[0]
    const selected = selection.type === 'airfield' && selection.value.name === airfield.name

    let iconHtml = `
      <div class="airportMarker">
          <div>
            <div class="airfieldIcon ${airfield.coalition.toLowerCase()} ${selected ? 'selected' : ''}">
              <span class="level">${airfield.level}</span>
            </div>
          </div>
          <div class="name">${airfield_name}</div>
      </div>
      `
    let icon = new L.DivIcon({className: 'airportIcon', html: iconHtml})

    markers.push(<Marker key={airfield.name} position={[airfield.position.lat, airfield.position.lon]}
      data={airfield}
      eventHandlers={{ click: (e) => { handleAirfieldClick(e.target.options.data) }}}
      icon={icon}/>)
  }

  for(let farp of sitRep.farps) {
    console.log(selection)
    const selected = selection.type === 'farp' && selection.value.name === farp.name

    let iconHtml = `
      <div class="airportMarker">
        <div>
          <div class="farpIcon ${farp.coalition.toLowerCase()} ${selected ? 'selected' : ''}">
            <span class="level">${farp.level}</span>
          </div>
        </div>
        <div class="name">${farp.name}</div>
      </div>
      `
    let icon = new L.DivIcon({className: 'airportIcon', html: iconHtml})

    markers.push(<Marker key={farp.name} position={[farp.position.lat, farp.position.lon]}
      data={farp}
      eventHandlers={{ click: (e) => { handleAirfieldClick(e.target.options.data, 'farp') }}}
      icon={icon}/>)
  }

  for(let airfield of sitRep.airfields_enemy) {
    // Some airfields have a dash in their name, we only want the first part
    // ex. Sochi-Adler -> Sochi - Too long of a name makes the UI ugly.
    const airfield_name = airfield.name.match(/^[^-]+/)[0]
    const selected = selection.type === 'airfield' && selection.value.name === airfield.name

    let iconHtml = `
      <div class="airportMarker">
          <div>
            <div class="airfieldIcon ${airfield.coalition.toLowerCase()} ${selected ? 'selected' : ''}">
            </div>
          </div>
          <div class="name">${airfield_name}</div>
      </div>
      `
    let icon = new L.DivIcon({ className: 'airportIcon', html: iconHtml })

    markers.push(<Marker key={airfield.name} position={[airfield.position.lat, airfield.position.lon]}
      data={airfield}
      eventHandlers={{ click: (e) => { handleAirfieldClick(e.target.options.data) }}}
      icon={icon}/>)
  }

  let gridPolygons = []

  for (let zone of sitRep.zones) {
    const lineStyle = zone.state.line_style.toLowerCase()

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

    const polygon = <Polygon key={zone.name} pathOptions={options} positions={pos}>
      <Popup>
        <div>{zone.state.zone_type}</div>
      </Popup>
    </Polygon>;
    gridPolygons.push(polygon);

    // Adding zone name markers
    const latSum = pos.reduce((sum, point) => sum + point[0], 0);
    const lonSum = pos.reduce((sum, point) => sum + point[1], 0);
    const centerLat = latSum / pos.length;
    const centerLon = lonSum / pos.length;

    const icon = new L.DivIcon({className: 'zoneNameIcon', html: `<div>${zone.name}</div>`})
    markers.push(<Marker key={`${zone.name}-icon`} position={[centerLat, centerLon]} icon={icon} interactive={false}/>)
  }

  return <div>
    {gridPolygons}
    {markers}
  </div>
}

function Map(props) {
  let sitRep = props.sitRep

  const map_center = theatres[sitRep.theatre.toLowerCase()].centre
  if (location.hash) {
    const hash = location.hash.slice(1).split('/')
    if (hash.length == 2) {
      map_center[0] = parseFloat(hash[0])
      map_center[1] = parseFloat(hash[1])
    }
  }

  return <MapContainer id="map" center={map_center}
          zoom={7.8}
          zoomDelta={0.8}
          zoomSnap={0}
          wheelPxPerZoomLevel={70}
          maxBounds={theatres[sitRep.theatre.toLowerCase()].bounds}
          maxBoundsViscosity={0.8}
          eventHandlers={{ click: () =>{ console.log("aaaa") } }}
          attributionControl={false}
          >

      <TileLayer
        attribution='&copy; mapbox'
        accessToken="pk.eyJ1IjoiY2Vsc29kYW50YXMiLCJhIjoiY2tnNWk4ZWlpMGcyZzJ5bDdjZTU5c2IwdCJ9.1dK2LqeGzVzILLxUToadzg"
        id={"celsodantas/cljbgm8oe008h01o049ln1xht/draft"}
        url='https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}'

      />
      <AttributionControl position="topright"/>
      <MapComponents sitRep={sitRep} />
    </MapContainer>

}

export default Map;
