import { Route, Routes } from "react-router-dom";
import PlayerSummary from "./PlayerSummary";
import PlayerPortal from "./PlayerPortal";

export default function PlayerRouter() {

    return (
        <div>
            <Routes>
                <Route path="/:user_id/*" element={<PlayerPortal />} />
                <Route path="/" element={<PlayerSummary />} />
            </Routes>
        </div>
    )
}