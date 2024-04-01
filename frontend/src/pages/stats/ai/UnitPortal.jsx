import { Box, Button, Grid, Tab, Tabs, Typography } from "@mui/material"
import { useContext, useEffect, useState } from "react"
import { useNavigate, useParams } from "react-router-dom"
import { AxiosContext } from "../../../contexts/AxiosContext"
import UnitKills from "./UnitKills"


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

export default function UnitPortal() {

    const params = useParams()
    console.log(params)
    const axios = useContext(AxiosContext)
    const navigate = useNavigate()
    const value = params?.["*"] || "kills"

    // const [value, setValue] = useState("flights");
    const [unitInfo, setUnitInfo] = useState(null)
    const [weaponInfo, setWeaponInfo] = useState(null)

    // Reload data
    useEffect(() => {
        axios.get(`/api/dcs_unit_type/${params.unit_id}`).then((res) => {
            if (!res) return
            setUnitInfo(res.data)
        })
    }, [params.unit_id])

    useEffect(() => {
        axios.get(`/api/weapon_type/${params.weapon_id}`).then((res) => {
            if (!res) return
            setWeaponInfo(res.data)
        })
    }, [params.weapon_id])

    const handleChange = (event, newValue) => {
        navigate(newValue);
    };

    return (
        <Box sx={{padding: 0}}>
            <Grid container>
                <Grid item xs={3}>
                    <Box pl={2} pt={1} pr={2}>
                        <Button sx={{width: "100%"}} variant="contained" onClick={() => navigate("..") }>Back to AI Weapon</Button>
                        <Box m={2} mt={1.5} sx={{background: "#333"}}>
                            <Box p={2}>
                                <Typography color='primary' sx={{paddingBottom: "10px"}} variant="h6">{unitInfo?.name}: {weaponInfo?.name}</Typography>
                            </Box>
                        </Box>
                    </Box>
                </Grid>
                <Grid item xs={9}>
                    <Tabs value={value} onChange={handleChange}>
                        <Tab label="Kills" value="kills" {...a11yProps("kills")} />
                    </Tabs>
                    <TabPanel value={value} index={"kills"}>
                        <UnitKills />
                    </TabPanel>
                </Grid>
            </Grid>
        </Box>

    )

}