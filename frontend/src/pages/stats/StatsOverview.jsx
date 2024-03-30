import { Box, Grid } from '@mui/material';
import KillsTable from './overview/KillsTable';
import { useParams } from 'react-router-dom';
import UnitsTable from './overview/UnitsTable';


export default function StatsOverview() {

    const params = useParams()

    return (
        <UnitsTable />
    )


}