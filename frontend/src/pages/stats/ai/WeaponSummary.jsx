import { Box, Typography } from "@mui/material"
import { useContext, useEffect, useState } from "react"
import { useNavigate, useParams, useSearchParams } from "react-router-dom"
import { StripedDataGrid } from "../../../components/grid/StripedDataGrid"
import { AxiosContext } from "../../../contexts/AxiosContext"
import { secondsToText } from "../../../utils"
import { GridToolbar } from "@mui/x-data-grid"

const columns = [
    {
      field: 'unit_weapon_name',
      headerName: 'Unit Weapon Name',
      flex: 1,
      valueGetter: (params) => `${params.row.unit_type.name}: ${params.row.weapon_type.display_name || params.row.weapon_type.name}`
    },
    {
      field: 'shots',
      headerName: 'Fired',
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
      width: 98,
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
      field: 'pk',
      headerName: 'PK%',
      align: 'right',
      headerAlign: 'right',
      width: 98,
      valueGetter: (params) => params.row?.shots
          ? Object.values(params.row?.kills ?? {})
              .reduce((prev, curr) => prev + Object.values(curr).reduce((a, b) => a+b, 0), 0)
              / params.row?.shots * 100
          : "",
      valueFormatter: (params) => params.value ? params.value.toFixed(1) : ""
    },
]

export default function WeaponSummary() {

    const navigate = useNavigate()
    const axios = useContext(AxiosContext)
    const [rows, setRows] = useState([])

    const [searchParams, setSearchParams] = useSearchParams()
    let params = {
      from: searchParams.get('from'),
      to: searchParams.get('to'),
    }

    // Reload our kills table
    useEffect(() => {
        axios.get('/api/weapon', {
          params: params
        }).then((res) => {
            if (!res) return
            setRows(res.data.map((v, idx) => { return {"id": idx+1, ...v} }))
        })
    }, [searchParams])

    const handleRowClick = (e) => {
      navigate({
        pathname: `by_unit/${e.row.unit_type.id}/weapon/${e.row.weapon_type.id}`,
        search: searchParams.toString()
      })
    }

    return (
        <Box m={2} sx={{background: "#333"}}>
            <Box p={2}>
                <Typography key="f" color='primary' sx={{paddingBottom: "10px"}} variant="h6">AI Unit Summary</Typography>
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
                    disableColumnMenu
                    autoHeight
                    pagination={true}
                    slots={{ toolbar: GridToolbar }}
                    disableColumnFilter
                    disableColumnSelector
                    disableDensitySelector
                    onRowClick={handleRowClick}
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