import { StripedDataGrid } from "./StripedDataGrid";

export default function StandardGrid({
    columns,
    sx,
    ...gridProps
}) {

    const gridStyle = {
        m:1,
        '& .hideSeparator > .MuiDataGrid-columnSeparator': {
            visibility: "hidden",
        },
        '& .MuiDataGrid-columnHeader.nooutline': {
            outline: "none !important",
        },
        '& .MuiDataGrid-cell:not(.MuiDataGrid-cell--editable):focus': {
            outline: "none",
        },
        '& .MuiDataGrid-row.edit > .MuiDataGrid-cell.actions': {
            borderBottom: "1px solid #ccc",
            borderRight: "2px solid #ccc",
        },
        '& .MuiDataGrid-actionsCell': {
            gridGap: 0,
        },
        '& .fullCell': {
            padding: '0 !important',
        },
        ...sx,
    }

    ///////////////////////////////////////////////////////////////////////////
    // Update column defs for our pinned row actions
    ///////////////////////////////////////////////////////////////////////////
    return (
        <StripedDataGrid
            sx={gridStyle}
            columns={columns}
            {...gridProps}
        />
    )
}