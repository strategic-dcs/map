import { useEffect } from 'react';
import './InfoPanel.css';
import { useSelectionContext } from './SelectionProvider';

function AirbaseInfo(props) {
  const airfield = props.airbase

  const level_0_restrictions = ["Guns Only"]
  const level_1_restrictions = ["Guns", "Dumb bombs", "Unguided Rockets"]
  const level_2_restrictions = ["Guns", "Dumb bombs", "Unguided Rockets", "Laser Guided Munitions", "Fox 1", "Fox 2, except 9X and R-27ET"]
  const level_3_restrictions = ["No restrictions"]

  let restrictions = []
  const restrictionsListHtml = []

  if (airfield.level === 0) {
    restrictions = level_0_restrictions
  } else if (airfield.level === 1) {
    restrictions = level_1_restrictions
  } else if (airfield.level === 2) {
    restrictions = level_2_restrictions
  } else if (airfield.level === 3) {
    restrictions = level_3_restrictions
  } else if (airfield.level === undefined) {
    restrictions = ["UNKNOWN"]
  }

  for (let restriction of restrictions) {
    restrictionsListHtml.push(<li key={restriction}>{restriction}</li>)
  }

  return <div className="content">
    <h1>{airfield.name}</h1>
    <span className="subheader">Level: {airfield.level ? airfield.level : "UNKNOWN"}</span>
    <div>
      <h3>Restrictions:</h3>
      <ul>
        {restrictionsListHtml}
      </ul>
    </div>
  </div>
}

function NoSelectionInfo() {
  return <div className="content">
    <h1>Info Panel</h1>
    <div>
      <h3>Select an airbase to view its information.</h3>
    </div>
  </div>
}

export default function InfoPanel() {
  const { selection } = useSelectionContext()

  let content = undefined

  if (selection.name === undefined) {
    content = <NoSelectionInfo/>
  } else {
    content = <AirbaseInfo airbase={selection}/>
  }

  return <div className="infoPanelContainer" key={selection.name}>
    <div className="content">
      {content}
    </div>
  </div>
}
