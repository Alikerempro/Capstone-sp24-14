import React from "react"
import {createRoot} from "react-dom/client";
import Navbar from "./Components/Navbar"
import MapView from "./MapView"
import DataView from "./DataView"
import CameraView from "./CameraView"
import ControlView from "./ControlView"

function IndexPage() {
    return (<>
    <Navbar href="/settings.html"/>
    <DataView/>
    <CameraView/>
    <MapView/>
    <ControlView/>
    </>);
}

const root = document.querySelector("#root")
createRoot(root).render(<IndexPage/>);
