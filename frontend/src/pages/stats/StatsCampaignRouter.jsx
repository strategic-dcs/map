import { Route, Routes, useParams } from "react-router-dom";
import StatsCampaignMenu from "./StatsCampaignMenu";
import StatsOverview from "./StatsOverview";
import PlayerRouter from "./player/PlayerRouter";

export default function StatsCampaignRouter({campaignList}) {

    const { campaign_id } = useParams();

    return (
        <div>
            <StatsCampaignMenu campaignList={campaignList} />
            <Routes>
                <Route path="overview" element={<StatsOverview />} />
                <Route path="player/*" element={<PlayerRouter />} />
            </Routes>
        </div>
    )


}