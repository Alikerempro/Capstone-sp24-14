import NavButton from "./NavButton"
import Battery from "./Battery"

export default function Navbar(props){
    return (<>
    <div className="leftNav">
        <h1>SP24-14: Autonomous Mapping of Water and fertilizer content in Soil</h1>
        <p><em>{props.pageName}</em></p>
    </div>
    <div className="rightNav">
        <Battery battPct={0.7}/>
        <NavButton href={props.href}/>
    </div>
    </>);
}