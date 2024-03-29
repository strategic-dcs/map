import { Box, Grid } from '@mui/material';
import KillsTable from './overview/KillsTable';
import { useParams } from 'react-router-dom';
import UnitsTable from './overview/UnitsTable';


export default function StatsOverview() {

    const params = useParams()

    return (
        <Box sx={{padding: 0}}>
            <Grid container>
                <Grid item xs={3}>
                    <KillsTable
                        title='Top 10 A/A Kills'
                        target={`/api/campaign/summary/top10/aa`}
                    />
                    <KillsTable
                        pilot_title='Commander'
                        title='Top 10 G/G Kills'
                        target={`/api/campaign/summary/top10/gg`}
                    />
                </Grid>
                <Grid item xs={6}>
                    <UnitsTable />
                </Grid>
                <Grid item xs={3}>
                    <KillsTable
                        title='Top 10 A/G Kills'
                        target={`/api/campaign/summary/top10/ag`}
                    />
                    <KillsTable
                        pilot_title='Commander'
                        title='Top 10 G/A Kills'
                        target={`/api/campaign/summary/top10/ga`}
                    />
                </Grid>
            </Grid>
        </Box>
    )


}