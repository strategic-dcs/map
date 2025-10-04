import { Box, Typography } from "@mui/material"
import { useContext, useEffect, useState } from "react"
import { useNavigate, useParams, useSearchParams } from "react-router-dom"
import { StripedDataGrid } from "../../../components/grid/StripedDataGrid"
import { AxiosContext } from "../../../contexts/AxiosContext"
import { secondsToText } from "../../../utils"
import { GridToolbar } from "@mui/x-data-grid"

const columns = [
    {
      field: 'user_name',
      headerName: 'Player Name',
      renderCell: ((params) => <Box sx={
        (() => {
          let vars = {}
          if (params.row?.user_side === "BLUE") vars['color'] = '#00aaff'
          else if (params.row?.user_side === "RED") vars['color'] = '#ff4444'
          return vars
        })()
      }>{params.value}</Box>),
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
      field: 'vanity_points_banked',
      headerName: 'Banked VP',
      align: 'right',
      headerAlign: 'right',
      width: 135,
      valueGetter: (params) => params.row?.vanity_points?.banked / 100 ?? 0
    },
    {
      field: 'vanity_points_lost',
      headerName: 'Lost VP',
      align: 'right',
      headerAlign: 'right',
      width: 105,
      valueGetter: (params) => ((params.row?.vanity_points?.total ?? 0) - (params.row?.vanity_points?.banked ?? 0)) / 100
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

    const axios = useContext(AxiosContext)
    const [rows, setRows] = useState([])
    const navigate = useNavigate()
    const [searchParams, _] = useSearchParams()

    // Reload our kills table
    useEffect(() => {
        axios.get('/api/player', {
          params: {
            from: searchParams.get('from'),
            to: searchParams.get('to'),
          }
        }).then((res) => {
            if (!res) return
            setRows(res.data.map((v, idx) => { return {"id": idx+1, ...v} }))
        })
    }, [searchParams ])

    const handleRowClick = (e) => {
        navigate({
          pathname: e.row.user_id.toString(),
          search: searchParams.toString(),
        })
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
                    disableColumnMenu
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