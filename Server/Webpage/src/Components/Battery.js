export default function Battery(props) {
    return (<>
    <div className="imgCap">
        <img id="batteryImg" src={(props.battPct >= 0.66 ? "Images/batFull.jpg" : (
            props.battPct >= 0.33 ? "Images/batMid.jpg" : "Images.batLow.jpg"
        ))} alt={(props.battPct >= 0.66 ? "Charge: HIGH" : (
            props.battPct >= 0.33 ? "Charge: MID" : "Charge: LOW"
        ))}/>
        <h2 className="caption" style={{color:"white"}}>{props.battPct*100 + "%"}</h2>
    </div>
    </>);
}