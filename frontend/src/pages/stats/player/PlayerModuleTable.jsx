import { Box, Typography } from "@mui/material"
import { useContext, useEffect, useMemo, useState } from "react"
import { useParams } from "react-router-dom"
import { StripedDataGrid } from "../../../components/grid/StripedDataGrid"
import { AxiosContext } from "../../../contexts/AxiosContext"
import { secondsToText } from "../../../utils"

const columns = [
    {
        field: 'unit_type',
        headerName: 'Module',
        flex: 0.75,
        minWidth: 0,
    },
    {
        headerName: 'Duration',
        align: 'right',
        headerAlign: 'right',
        field: 'duration',
        width: 150,
        valueGetter: (params) => params.row?.duration ?? 0,
        valueFormatter: (params) => secondsToText(params.value),
    },
]

export default function PlayerModuleTable({coalition, name}) {

    const params = useParams()
    const axios = useContext(AxiosContext)
    const [rows, setRows] = useState([])

    // Reload data
    useEffect(() => {
        axios.get(`/api/player/${params.user_id}/modules`, {
            params: {
                campaign_id: params.campaign_id === "all" ? undefined: params.campaign_id
            }
        }).then((res) => {
            if (!res) return
            setRows(res.data.map((v, idx) => { return {"id": idx+1, ...v} }))
        })
    }, [params.campaign_id, params.user_id])

    let color = (() => {
        if (coalition === "BLUE") return '#00aaff'
        if (coalition === "RED") return '#ff4444'
        return '#eeeeee'
    })()


    return (
        <Box m={2} mt={1.5} sx={{background: "#333"}}>
            <Box p={2}>
                <Typography color={{color}} sx={{paddingBottom: "10px"}} variant="h6">{name}</Typography>
                <StripedDataGrid
                    columns={columns}
                    rows={rows}
                    hideFooter={true}
                    disableColumnMenu
                    autoHeight
                    density="compact"
                />
            </Box>
        </Box>
    )
}