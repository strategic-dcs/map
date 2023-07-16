import { useEffect } from 'react';
import './InfoPanel.css';
import { useSelectionContext } from './SelectionContext';

function AirbaseInfo(props) {
  const airbase = props.airbase

  const level_0_restrictions = ["Guns Only"]
  const level_1_restrictions = ["Guns", "Dumb bombs", "Unguided Rockets"]
  const level_2_restrictions = ["Guns", "Dumb bombs", "Unguided Rockets", "Laser Guided Munitions", "Fox 1", "Fox 2, except 9X and R-27ET"]
  const level_3_restrictions = ["No restrictions"]

  let restrictions = []
  const restrictions_list_html = []

  if (airbase.level === 0) {
    restrictions = level_0_restrictions
  } else if (airbase.level === 1) {
    restrictions = level_1_restrictions
  } else if (airbase.level === 2) {
    restrictions = level_2_restrictions
  } else if (airbase.level === 3) {
    restrictions = level_3_restrictions
  } else if (airbase.level === undefined) {
    restrictions = ["UNKNOWN"]
  }

  for (let restriction of restrictions) {
    restrictions_list_html.push(<li key={restriction}>{restriction}</li>)
  }

  return <div className="content">
    <h1>{airbase.name}</h1>
    <span className="subheader">Level: {airbase.level ? airbase.level : "UNKNOWN"}</span>
    <div>
      <h3>Restrictions:</h3>
      <ul>
        {restrictions_list_html}
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

  if (selection.type === undefined) {
    content = <NoSelectionInfo/>
  } else {
    content = <AirbaseInfo airbase={selection.value}/>
  }

  return <div className="infoPanelContainer">
    <div className="content">
      {content}
    </div>
  </div>
}
