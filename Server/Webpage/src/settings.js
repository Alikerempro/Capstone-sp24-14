import React from "react"
import {createRoot} from "react-dom/client";
import Navbar from "./Components/Navbar"
import View from "./Components/View"

function SettingsPage() {
    //This is a template. Each view contains a button, a header, and some text
    return (<>
    <Navbar href="/index.html" pageName="settings.html"/>
    <View draggable={false}>
        <h3></h3>
        <p></p>
        <button></button>
    </View>
    </>);
}

const root = document.querySelector("#root")
createRoot(root).render(<SettingsPage/>);
