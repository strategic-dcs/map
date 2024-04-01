
import { MenuItem, Tab, Tabs } from '@mui/material';
import Select from '@mui/material/Select';
import { Link, useLocation, useNavigate, useParams } from 'react-router-dom';

export default function StatsCampaignMenu({campaignList}) {

    const params = useParams()
    const navigate = useNavigate()
    const location = useLocation()

    const handleChange = (evt) => {
        // We replace our existing ID with thte new ID keepign us on the same tag
        let elems = location.pathname.split("/")
        elems[2] = evt.target.value
        let new_path = elems.join("/")
        navigate(new_path, {replace: true})
    }

    return (
        <div style={{width: "100%", backgroundColor: "#666666", display: 'flex'}}>
            <Select
                label="Campaign"
                value={campaignList ? params.campaign_id : "all"}
                sx={{
                    height: "32px",
                    width: "240px",
                }}
                onChange={handleChange}
            >
                <MenuItem key="all" value="all">Campaign: All</MenuItem>
                {campaignList && campaignList.map((x) => {
                    let date = new Date(x.start)
                    return <MenuItem key={x.id} value={x.id.toString()}>{date.toISOString().split("T")[0]}: {x.mission.display_name}</MenuItem>
                })}
            </Select>
            <Tabs
                sx={{
                    height: '32px',
                    minHeight: '32px',
                    '& .MuiTab-root': {
                        height: '32px',
                        minHeight: '32px',
                    },
                }}
                value={location.pathname.split("/")[3]}
                TabIndicatorProps={{
                    sx: {
                        height: "3px",
                    }
                }}
            >
                <Tab LinkComponent={Link} to="overview" value="overview" label="Overview" />
                <Tab LinkComponent={Link} to="ai" value="ai" label="AI Units" />
                <Tab LinkComponent={Link} to="player" value="player" label="Player" />
            </Tabs>
        </div>
    )
}