
import { Box, Grid, Typography } from "@mui/material"
import { useContext, useEffect, useState } from "react"
import { useNavigate, useParams } from "react-router-dom"
import { StripedDataGrid } from "../../../components/grid/StripedDataGrid"
import { AxiosContext } from "../../../contexts/AxiosContext"
import { secondsToText } from "../../../utils"

const columns = [
    {
        field: 'kill_at',
        headerName: 'Time',
        minWidth: 250,
        valueFormatter: (params) => new Date(params.value).toUTCString()
    },
    {
        field: 'unit',
        headerName: 'Your Unit',
        valueGetter: (params) => {
            let suffix = params.row.target_unit.unit_suffix
            if (suffix) return params.row.target_unit.unit_suffix
            return params.row.target_unit.unit_type.type_name
        },
        minWidth: 250,
        flex: 1,
    },
    {
        field: 'killer',
        headerName: 'Killer',
        flex: 1,
        valueGetter: (params) => params.row.kill_player?.name ?? "AI"
    },
    {
        field: 'weapon',
        headerName: 'Weapon',
        flex: 1,
        valueGetter: (params) => params.row.weapon.weapon_name
    },
    {
        field: 'killer_unit',
        headerName: 'Unit',
        flex: 1,
        valueGetter: (params) => params.row.weapon.unit.unit_type.type_name
    },
    {
      headerName: 'Method',
      field: 'assoc_method',
      flex: 1,
    },
]

export default function PlayerDeaths() {

    const params = useParams()
    const axios = useContext(AxiosContext)
    const [rows, setRows] = useState([])
    const navigate = useNavigate()

    // Reload our kills table
    useEffect(() => {
        axios.get(`/api/player/${params.user_id}/deaths`, {
            params: {
                campaign_id: params.campaign_id !== "all" ? params.campaign_id : null
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