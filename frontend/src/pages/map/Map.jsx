import './Map.css';

import { MapContainer, TileLayer, Marker, Polygon, Popup, AttributionControl } from 'react-leaflet'
import { useMapEvents } from 'react-leaflet/hooks'
import blueAirportIcon from '/blue-airfield.svg'
import redAirportIcon from '/red-airfield.svg'
import neutralAirportIcon from '/neutral-airfield.svg'
import ServerInfo from './ServerInfo';
import { useSelectionContext } from '../../contexts/SelectionContext';
import { useContext, useEffect, useState } from 'react';
import { AxiosContext } from '../../contexts/AxiosContext';


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

function Map() {

  const [sitRep, setSitRep] = useState(null);
  const axios = useContext(AxiosContext)

  useEffect(() => {
    // Cookies.get('access_token') ? setIsLoggedIn(true) : setIsLoggedIn(false);

    axios.get(`/api/sitrep`).then((res) => {
      if (!res) return
      setSitRep(res.data)
    })

    // in dev mode, refresh every 10 seconds.
    const internal = setInterval(() => {
      axios.get(`/api/sitrep`).then((res) => {
        if (!res) return

        // Only updating sitRep if the payload SHA has changed.
        // Otherwise, it would cause the whole app to reload and rebuild.
        setSitRep((prevSitRep) => {
          if (prevSitRep?.sha != res.data.sha) {
            return res.data
          } else {
            return prevSitRep
          }
        })

      })
    }, (import.meta.env.DEV ? 10 : 30) * 1000);

    return () => { clearInterval(internal) }

  }, [])

  if (!sitRep) return (<div>Loading</div>)

  const map_center = [sitRep.center.lat, sitRep.center.lon]
  if (location.hash) {
    const hash = location.hash.slice(1).split('/')
    if (hash.length == 2) {
      map_center[0] = parseFloat(hash[0])
      map_center[1] = parseFloat(hash[1])
    }
  }

  return (
    <div>
      <MapContainer id="map" center={map_center}
            zoom={7.8}
            zoomDelta={0.8}
            zoomSnap={0}
            wheelPxPerZoomLevel={70}
            maxBounds={[[sitRep.bounds.min.lat, sitRep.bounds.min.lon],[sitRep.bounds.max.lat, sitRep.bounds.max.lon]]}
            maxBoundsViscosity={0.8}
            eventHandlers={{ click: () =>{ console.log("aaaa") } }}
            attributionControl={false}
            >

        <TileLayer
          attribution='Esri, HERE, Garmin, &copy; OpenStreetMap contributors, and the GIS user community'
          url='http://services.arcgisonline.com/arcgis/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}'

        />
        <AttributionControl position="topright"/>
        <MapComponents sitRep={sitRep} />
      </MapContainer>
      <ServerInfo
        online_users={sitRep.online_users}
        seconds_left_until_restart={sitRep.seconds_left_until_restart}/>
    </div>)

}

export default Map;
