import { Box, Typography } from "@mui/material"
import { useContext, useEffect, useState } from "react"
import { useParams, useSearchParams } from "react-router-dom"
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
      field: 'aap',
      headerName: 'AA(P)',
      align: 'right',
      headerAlign: 'right',
      width: 98,
      valueGetter: (params) => params.row?.kills?.aa?.player || ""
    },
    {
      field: 'aaa',
      headerName: 'AA(AI)',
      align: 'right',
      headerAlign: 'right',
      width: 98,
      valueGetter: (params) => params.row?.kills?.aa?.ai || ""
    },
    {
      field: 'aat',
      headerName: 'AA(TK)',
      align: 'right',
      headerAlign: 'right',
      width: 98,
      valueGetter: (params) => params.row?.kills?.aa?.tk || ""
    },
    {
      field: 'agp',
      headerName: 'AG(P)',
      align: 'right',
      headerAlign: 'right',
      width: 90,
      valueGetter: (params) => params.row?.kills?.ag?.player || ""
    },
    {
      field: 'aga',
      headerName: 'AG(AI)',
      align: 'right',
      headerAlign: 'right',
      width: 98,
      valueGetter: (params) => params.row?.kills?.ag?.ai || ""
    },
    {
      field: 'agt',
      headerName: 'AG(TK)',
      align: 'right',
      headerAlign: 'right',
      width: 98,
      valueGetter: (params) => params.row?.kills?.ag?.tk || ""
    },
    {
      field: 'gap',
      headerName: 'GA(P)',
      align: 'right',
      headerAlign: 'right',
      width: 90,
      valueGetter: (params) => params.row?.kills?.ga?.player || ""
    },
    {
      field: 'gaa',
      headerName: 'GA(AI)',
      align: 'right',
      headerAlign: 'right',
      width: 98,
      valueGetter: (params) => params.row?.kills?.ga?.ai || ""
    },
    {
      field: 'ggp',
      headerName: 'GG(P)',
      align: 'right',
      headerAlign: 'right',
      width: 90,
      valueGetter: (params) => params.row?.kills?.gg?.player || ""
    },
    {
      field: 'gga',
      headerName: 'GG(AI)',
      align: 'right',
      headerAlign: 'right',
      width: 98,
      valueGetter: (params) => params.row?.kills?.gg?.ai || ""
    },
    {
      field: 'ggt',
      headerName: 'GG(TK)',
      align: 'right',
      headerAlign: 'right',
      width: 98,
      valueGetter: (params) => params.row?.kills?.gg?.tk || ""
    },
    {
      field: 'suicides',
      headerName: 'SELF',
      align: 'right',
      headerAlign: 'right',
      width: 98,
      valueGetter: (params) => params.row?.kills?.suicide || ""
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

    const axios = useContext(AxiosContext)
    const [rows, setRows] = useState([])
    const [searchParams, setSearchParams] = useSearchParams()

    // Reload our kills table
    useEffect(() => {
        axios.get('/api/campaign/summary/units', {
          params: {
            from: searchParams.get('from'),
            to: searchParams.get('to'),
          }
        }).then((res) => {
            if (!res) return
            setRows(res.data.map((v, idx) => { return {"id": idx+1, ...v} }))
        })
    }, [searchParams])

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