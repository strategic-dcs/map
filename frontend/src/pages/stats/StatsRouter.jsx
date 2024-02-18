import { Navigate, Route, Routes } from "react-router-dom";
import StatsCampaignRouter from "./StatsCampaignRouter";
import { useContext, useEffect, useState } from "react";
import { AxiosContext } from "../../contexts/AxiosContext";

function StatsRedirect({campaignList}) {

    if (campaignList) {
        return <Navigate to={`${campaignList[0].id}/overview`} replace />
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
            <Routes>
                <Route path=":campaign_id/*" element={<StatsCampaignRouter campaignList={campaignList} />} />
                <Route path="" element={<StatsRedirect campaignList={campaignList} />} />
            </Routes>
        </div>
    )
}