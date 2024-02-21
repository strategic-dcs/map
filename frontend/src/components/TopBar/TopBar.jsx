import './TopBar.css';

import { Tab, Tabs } from '@mui/material';
import { Link, useLocation } from 'react-router-dom';

function TopBar() {

    const loc = useLocation()
    const selected = loc.pathname.split("/")[1]

    return (
        <div>
            <div className="banner">

                <img className="sdcslogo" src="/sdcs-logo.png"></img>
                <div style={{width: "150px"}}>
                    <div className="serverName">Strategic DCS</div>
                    <div style={{fontSize: "12px"}}>Server: Modern</div>
                </div>

                <Tabs
                    value={selected}
                    TabIndicatorProps={{
                        sx: {
                            height: "4px",
                        }
                    }}
                >
                    <Tab LinkComponent={Link} to="map" value="map" label="Map" />
                    <Tab LinkComponent={Link} to="stats" value="stats" label="Stats" />
                    <Tab LinkComponent={Link} to="https://wiki.strategic-dcs.com" value="wiki" label="Wiki" />
                    <Tab LinkComponent={Link} to="https://strategic-dcs.com/tacview" value="tacview" label="Tacviews" />
                </Tabs>
            </div>
            <div style={{width: "100%", height:"2px", backgroundColor: "#a4a4a4"}} />
        </div>
    )
}

export default TopBar;