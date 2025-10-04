import { Navigate, Route, Routes } from "react-router-dom";
import { useContext, useEffect, useState } from "react";
import { AxiosContext } from "../../contexts/AxiosContext";
import StatsOverview from "./StatsOverview";
import PlayerRouter from "./player/PlayerRouter";
import WeaponRouter from "./ai/WeaponRouter";
import StatsCampaignMenu from "./StatsCampaignMenu";


function StatsRedirect({campaignList}) {

    if (campaignList) {
        return <Navigate to={`overview`} replace />
    }

    return "Loading"
}

export default function StatsRouter() {

    // We get our list of campaigns here, populate and provide
    // our route to the StatsCampaign page with the selected
    // campaign to populate our campaign dropdown

    const axiosContext = useContext(AxiosContext);
    const [campaignList, setCampaignList] = useState()

    useEffect(() => {
        axiosContext.get('/api/campaign').then((res) => {
            if (!res) return;
            setCampaignList(res.data)
        })
    }, [])

    return (
        <div>
            <StatsCampaignMenu campaignList={campaignList} />
            <Routes>
                <Route path="overview/*" element={<StatsOverview />} />
                <Route path="player/*" element={<PlayerRouter />} />
                <Route path="ai/*" element={<WeaponRouter />} />
                <Route path="" element={<StatsRedirect campaignList={campaignList} />} />
            </Routes>
        </div>
    )
}