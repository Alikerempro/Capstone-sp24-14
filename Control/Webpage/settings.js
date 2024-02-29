import View from "./Components/View"



import React from "react"
import {createRoot} from "react-dom/client";
import Navbar from "./Components/Navbar"
import MapView from "./MapView"
import DataView from "./DataView"
import CameraView from "./CameraView"
import ControlView from "./ControlView"

function IndexPage() {
    //This is a template. Each view contains a button, a header, and some text
    return (<>
    <Navbar href="/settings.html"/>
    <View draggable={false}>
        <h3></h3>
        <p></p>
        <button></button>
    </View>
    </>);
}

const root = document.querySelector("#root")
createRoot(root).render(<IndexPage/>);
