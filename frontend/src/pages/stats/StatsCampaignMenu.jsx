
import { MenuItem, Tab, Tabs, Typography } from '@mui/material';
import Select from '@mui/material/Select';
import { Link, useLocation, useNavigate, useParams, useSearchParams } from 'react-router-dom';

export default function StatsCampaignMenu({campaignList}) {

    const location = useLocation()
    const navigate = useNavigate()
    let [searchParams, setSearchParams] = useSearchParams();

    const handleChangeFrom = (evt) => {
        setSearchParams((searchParams) => {
            if (evt.target.value === 'one') {
                searchParams.delete('from')
            } else {
                searchParams.set('from', evt.target.value)
            }
            return searchParams;
        });
    }

    const handleChangeTo = (evt) => {
        setSearchParams((searchParams) => {
            searchParams.set("to", evt.target.value);
            return searchParams;
        });
    }

    const handleClick = (evt, target) => {
        console.log(searchParams)
        navigate({
            pathname: target,
            search: searchParams.toString()
        })
    }

    let from = searchParams.get('from')
    let to = searchParams.get('to')

    return (
        <div style={{width: "100%", backgroundColor: "#666666", display: 'flex'}}>
            <Typography pr={1} pl={1} alignContent='center' sx={{color: 'white'}}>Range:</Typography>
            <Select
                label="Campaign Start"
                value={campaignList && from ? from : "one"}
                sx={{
                    height: "32px",
                    width: "240px",
                }}
                onChange={handleChangeFrom}
            >
                <MenuItem key="one" value="one">Campaign: One</MenuItem>
                <MenuItem key="0" value="0">Campaign: All</MenuItem>
                {campaignList && campaignList.map((x) => {
                    let date = new Date(x.start)
                    return <MenuItem key={x.id} value={x.id.toString()}>{date.toISOString().split("T")[0]}: {x.mission.display_name}</MenuItem>
                })}
            </Select>
            <Typography pr={1} pl={1} alignContent='center' sx={{color: 'white'}}>-</Typography>
            <Select
                label="Campaign"
                value={campaignList ? (to ? to : campaignList[0].id) : "" }
                sx={{
                    height: "32px",
                    width: "240px",
                }}
                onChange={handleChangeTo}
            >
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
                onChange={handleClick}
                value={location.pathname.split("/")[2]}
                TabIndicatorProps={{
                    sx: {
                        height: "3px",
                    }
                }}
            >
                <Tab LinkComponent={Link} value="overview" label="Overview" />
                <Tab LinkComponent={Link} value="ai" label="AI Units" />
                <Tab LinkComponent={Link} value="player" label="Player" />
            </Tabs>
        </div>
    )
}