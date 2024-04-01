import { Route, Routes } from "react-router-dom";
import WeaponSummary from "./WeaponSummary";
import UnitPortal from "./UnitPortal";

export default function WeaponRouter() {

    return (
        <div>
            <Routes>
                <Route path="/by_unit/:unit_id/weapon/:weapon_id/*" element={<UnitPortal />} />
                <Route path="/" element={<WeaponSummary />} />
            </Routes>
        </div>
    )
}