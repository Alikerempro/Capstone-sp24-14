import React from "react"
import {createRoot} from "react-dom/client";
import Navbar from "./Components/Navbar"
import MapView from "./Components/MapView"
import DataView from "./Components/DataView"
import CameraView from "./Components/CameraView"
import ControlView from "./Components/ControlView"

function IndexPage() {
    return (<>
    <Navbar href="/settings.html"/>
    <DataView/>
    <CameraView/>
    <MapView/>
    <ControlView/>
    </>);
}

const root = document.getElementById('root')
createRoot(root).render(<IndexPage/>);
