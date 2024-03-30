import { Box, Typography } from "@mui/material"
import { useContext, useEffect, useMemo, useState } from "react"
import { useParams } from "react-router-dom"
import { StripedDataGrid } from "../../../components/grid/StripedDataGrid"
import { AxiosContext } from "../../../contexts/AxiosContext"


export default function KillsTable({
    title,
    target,
    pilot_title,
}) {

    const params = useParams()
    const axios = useContext(AxiosContext)
    const [rows, setRows] = useState([])

    // Reload our kills table
    useEffect(() => {
        axios.get(target, {
            params: {
                campaign_id: params.campaign_id === 'all' ? undefined : params.campaign_id
            }
        }).then((res) => {
            if (!res) return
            setRows(res.data.map((v, idx) => { return {"id": idx+1, ...v} }))
        })
    }, [target, params.campaign_id])


    const columns = useMemo(() => [
        {
          field: 'pilot',
          headerName: pilot_title ?? 'Pilot',
          flex: 0.75,
          minWidth: 0,
        },
        {
          field: 'pvp',
          headerName: 'PVP',
          align: 'right',
          headerAlign: 'right',
          flex: 0.25,
          minWidth: 0,
          valueGetter: (params) => params.row?.kills?.pvp || ""
        },
        {
          field: 'ai',
          headerName: 'AI',
          align: 'right',
          headerAlign: 'right',
          flex: 0.25,
          minWidth: 0,
          valueGetter: (params) => params.row?.kills?.ai || ""
        }
    ], [pilot_title])

    return (
        <Box m={2} sx={{background: "#333"}}>
            <Box p={2}>
                <Typography color='primary' sx={{paddingBottom: "10px"}} variant="h6">{title}</Typography>
                <StripedDataGrid
                    initialState={{
                        pagination: { paginationModel: { pageSize: 10 } },
                    }}
                    columns={columns}
                    rows={rows}
                    //hideFooter={true}
                    disableColumnMenu
                    autoHeight
                    density="compact"
                    pageSizeOptions={[10]}
                />
            </Box>
        </Box>
    )

}