import { Box, Button, Grid, Tab, Tabs } from "@mui/material"
import { useContext, useEffect, useState } from "react"
import { useLocation, useNavigate, useParams } from "react-router-dom"
import { AxiosContext } from "../../../contexts/AxiosContext"
import PlayerModuleTable from "./PlayerModuleTable"
import PlayerKills from "./PlayerKills"
import PlayerFlights from "./PlayerFlights"
import PlayerDeaths from "./PlayerDeaths"


function TabPanel(props) {
    const { children, value, index, ...other } = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`player-tabs-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            {...other}
        >
            {value === index && (
                <Box sx={{ p: 1 }}>
                    {children}
                </Box>
            )}
        </div>
    );
}

function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
}

export default function PlayerPortal() {

    const params = useParams()
    const axios = useContext(AxiosContext)
    const navigate = useNavigate()
    const value = params?.["*"] || "flights"

    // const [value, setValue] = useState("flights");
    const [playerInfo, setPlayerInfo] = useState(null)

    // Reload data
    useEffect(() => {
        axios.get(`/api/player/${params.user_id}`).then((res) => {
            if (!res) return
            setPlayerInfo(res.data)
        })
    }, [params.user_id])

    const handleChange = (event, newValue) => {
        navigate(newValue);
    };

    return (
        <Box sx={{padding: 0}}>
            <Grid container>
                <Grid item xs={3}>
                    <Box pl={2} pt={1} pr={2}>
                        <Button sx={{width: "100%"}} variant="contained" onClick={() => navigate("..") }>Back to Player List</Button>
                    </Box>
                    <PlayerModuleTable name={playerInfo?.name} />
                </Grid>
                <Grid item xs={9}>
                    <Tabs value={value} onChange={handleChange} aria-label="basic tabs example">
                        <Tab label="Flights" value="flights" {...a11yProps("flights")} />
                        <Tab label="Kills" value="kills" {...a11yProps("kills")} />
                        <Tab label="Deaths" value="deaths" {...a11yProps("deaths")} />
                    </Tabs>
                    <TabPanel value={value} index={"flights"}>
                        <PlayerFlights />
                    </TabPanel>
                    <TabPanel value={value} index={"kills"}>
                        <PlayerKills />
                    </TabPanel>
                    <TabPanel value={value} index={"deaths"}>
                        <PlayerDeaths />
                    </TabPanel>


                </Grid>
            </Grid>
        </Box>

    )

}