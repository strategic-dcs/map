import { Box, Typography } from "@mui/material"
import { useContext, useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { StripedDataGrid } from "../../../components/grid/StripedDataGrid"
import { AxiosContext } from "../../../contexts/AxiosContext"
import { secondsToText } from "../../../utils"

const columns = [
    {
      field: 'unit_type',
      headerName: 'Unit Type',
      flex: 1,
    },
    {
      field: 'flights',
      headerName: 'Flights',
      align: 'right',
      headerAlign: 'right',
      width: 100
    },
    {
      headerName: 'A2A',
      align: 'right',
      headerAlign: 'right',
      width: 70,
      field: 'a2a',
      valueGetter: (params) => params.row?.kills?.a2a || ""
    },
    {
      field: 'A2G',
      headerName: 'A2G',
      align: 'right',
      headerAlign: 'right',
      field: 'a2g',
      width: 70,
      valueGetter: (params) => params.row?.kills?.a2g || ""
    },
    {
      field: 'G2A',
      headerName: 'G2A',
      align: 'right',
      headerAlign: 'right',
      field: 'g2a',
      width: 70,
      valueGetter: (params) => params.row?.kills?.g2a || ""
    },
    {
      field: 'G2G',
      headerName: 'G2G',
      align: 'right',
      headerAlign: 'right',
      field: 'g2g',
      width: 70,
      valueGetter: (params) => params.row?.kills?.g2g || ""
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

export default function UnitsTable() {

    const params = useParams()
    const axios = useContext(AxiosContext)
    const [rows, setRows] = useState([])

    // Reload our kills table
    useEffect(() => {
        axios.get(`/api/campaign/${params.campaign_id !== "all" ? params.campaign_id : ''}/summary/top10/units`).then((res) => {
            if (!res) return
            setRows(res.data.map((v, idx) => { return {"id": idx+1, ...v} }))
        })
    }, [params.campaign_id])

    return (
        <Box m={2} sx={{background: "#333"}}>
            <Box p={2}>
                <Typography key="f" color='primary' sx={{paddingBottom: "10px"}} variant="h6">Player controlled unit summary</Typography>
                <StripedDataGrid
                    initialState={{
                        pagination: { paginationModel: { pageSize: 15 } },
                    }}
                    key="grid"
                    columns={columns}
                    rows={rows}
                    pageSizeOptions={[15]}
                    disableColumnMenu
                    autoHeight
                    pagination={true}
                />
            </Box>
        </Box>
    )

}