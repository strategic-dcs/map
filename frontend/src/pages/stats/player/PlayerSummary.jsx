import { Box, Typography } from "@mui/material"
import { useContext, useEffect, useState } from "react"
import { useNavigate, useParams } from "react-router-dom"
import { StripedDataGrid } from "../../../components/grid/StripedDataGrid"
import { AxiosContext } from "../../../contexts/AxiosContext"
import { secondsToText } from "../../../utils"
import { GridToolbar } from "@mui/x-data-grid"

const columns = [
    {
      field: 'user_name',
      headerName: 'Player Name',
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
      width: 80,
      field: 'a2a',
      valueGetter: (params) => params.row?.kills?.a2a || ""
    },
    {
      field: 'A2G',
      headerName: 'A2G',
      align: 'right',
      headerAlign: 'right',
      field: 'a2g',
      width: 80,
      valueGetter: (params) => params.row?.kills?.a2g || ""
    },
    {
      field: 'G2A',
      headerName: 'G2A',
      align: 'right',
      headerAlign: 'right',
      field: 'g2a',
      width: 80,
      valueGetter: (params) => params.row?.kills?.g2a || ""
    },
    {
      field: 'G2G',
      headerName: 'G2G',
      align: 'right',
      headerAlign: 'right',
      field: 'g2g',
      width: 80,
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

export default function PlayerSummary() {

    const params = useParams()
    const axios = useContext(AxiosContext)
    const [rows, setRows] = useState([])
    const navigate = useNavigate()

    // Reload our kills table
    useEffect(() => {
        axios.get('/api/player', {
          params: {
            campaign_id: params.campaign_id === "all" ? undefined : params.campaign_id
          }
        }).then((res) => {
            if (!res) return
            setRows(res.data.map((v, idx) => { return {"id": idx+1, ...v} }))
        })
    }, [params.campaign_id])

    const handleRowClick = (e) => {
        navigate(e.row.user_id.toString())
    }

    return (
        <Box m={2} sx={{background: "#333"}}>
            <Box p={2}>
                <Typography key="f" color='primary' sx={{paddingBottom: "10px"}} variant="h6">
                    Registered Players
                </Typography>
                <StripedDataGrid
                    initialState={{
                        pagination: { paginationModel: { pageSize: 15 } },
                    }}
                    sx={{
                      '.MuiDataGrid-toolbarContainer > .MuiBox-root': {
                        display: "none"
                      }
                    }}
                    key="grid"
                    columns={columns}
                    rows={rows}
                    pageSizeOptions={[15]}
                    autoHeight
                    pagination={true}
                    onRowClick={handleRowClick}
                    disableColumnFilter
                    disableColumnSelector
                    disableDensitySelector
                    slots={{ toolbar: GridToolbar }}
                    slotProps={{
                      toolbar: {
                        printOptions: { disableToolbarButton: true },
                        csvOptions: { disableToolbarButton: true },
                        showQuickFilter: true,
                      },
                    }}
                />
            </Box>
        </Box>
    )

}