
import { Box, Grid, Typography } from "@mui/material"
import { useContext, useEffect, useState } from "react"
import { useNavigate, useParams } from "react-router-dom"
import { StripedDataGrid } from "../../../components/grid/StripedDataGrid"
import { AxiosContext } from "../../../contexts/AxiosContext"
import { secondsToText } from "../../../utils"

const columns = [
    {
        field: 'start',
        headerName: 'Start',
        minWidth: 250,
        valueFormatter: (params) => new Date(params.value).toUTCString()
    },
    {
        field: 'end',
        headerName: 'End',
        minWidth: 250,
        valueFormatter: (params) => new Date(params.value).toUTCString()
    },
    {
        field: 'unit',
        headerName: 'Unit',
        valueGetter: (params) => {
            let suffix = params.row.unit.unit_suffix
            if (suffix) return params.row.unit.unit_suffix
            return params.row.unit.unit_type.type_name
        },
        minWidth: 250,
    },
    {
        field: 'leg_count',
        headerName: 'Legs',
        align: 'right',
        headerAlign: 'right',
        flex: 1,
    },
    {
        field: 'distance',
        headerName: 'Distance (km)',
        align: 'right',
        headerAlign: 'right',
        flex: 1,
        valueFormatter: (params) => (Math.round(params.value/1000)).toLocaleString(),
    },
    {
        field: 'distance_abs',
        headerName: 'Distance (abs, km)',
        align: 'right',
        headerAlign: 'right',
        valueFormatter: (params) => (Math.round(params.value/1000)).toLocaleString(),
        flex: 1,
    },
]

export default function PlayerFlights() {

    const params = useParams()
    const axios = useContext(AxiosContext)
    const [rows, setRows] = useState([])

    // Reload our kills table
    useEffect(() => {
        axios.get(`/api/player/${params.user_id}/flights`, {
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