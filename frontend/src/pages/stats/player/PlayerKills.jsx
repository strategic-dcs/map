
import { Box, Grid, Typography } from "@mui/material"
import { useContext, useEffect, useState } from "react"
import { useNavigate, useParams } from "react-router-dom"
import { StripedDataGrid } from "../../../components/grid/StripedDataGrid"
import { AxiosContext } from "../../../contexts/AxiosContext"
import { secondsToText } from "../../../utils"

const columns = [
    {
      field: 'kill_at',
      headerName: 'UTC',
      valueFormatter: (params) => new Date(params.value).toUTCString(),
      minWidth: 250,
    },
    {
        field: 'killer_unit_type',
        headerName: 'Player Unit',
        minWidth: 220
    },
    {
        field: 'target_unit_type',
        headerName: 'Target Unit',
        minWidth: 220
    },
    {
        field: 'weapon_name',
        headerName: 'Weapon Name',
        minWidth: 200,
        flex: 1,
        valueGetter: (params) => params.row.weapon_type.display_name || params.row.weapon_type.name
    },
    {
        field: 'target_player_name',
        headerName: 'Player Name',
        minWidth: 200,
        flex: 1,
    },
    {
      headerName: 'Method',
      field: 'assoc_method',
      flex: 1,
    },
    {
      headerName: 'Ground Kill',
      align: 'right',
      headerAlign: 'right',
      field: 'target_on_ground',
      type: 'boolean',
      flex: 1,
    },
    {
      headerName: 'Team Kill',
      align: 'right',
      headerAlign: 'right',
      field: 'team_kill',
      type: 'boolean',
      flex: 1,
    },
]

export default function PlayerKills() {

    const params = useParams()
    const axios = useContext(AxiosContext)
    const [rows, setRows] = useState([])

    // Reload our kills table
    useEffect(() => {
        axios.get(`/api/player/${params.user_id}/kills`, {
            params: {
                campaign_id: params.campaign_id === "all" ? undefined : params.campaign_id
            }
        }).then((res) => {
            if (!res) return
            setRows(res.data.map((v, idx) => { return {"id": idx+1, ...v} }))
        })
    }, [params.campaign_id, params.user_id])

    return (
        <Box m={0} sx={{background: "#333"}}>
            <Box p={2}>
                <StripedDataGrid
                    initialState={{
                        pagination: { paginationModel: { pageSize: 15 } },
                    }}
                    key="grid"
                    columns={columns}
                    rows={rows}
                    pageSizeOptions={[15]}
                    autoHeight
                    pagination={true}
                />
            </Box>
        </Box>
    )
}