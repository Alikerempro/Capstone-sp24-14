import View from "./View"
import NavButton from "./NavButton";

export default function ControlView(){
    return (<>
    <View dragable={true}>
        <NavButton id="robotPause"/>
        <NavButton id="robotManual"/>
        <NavButton id="robotUp" imgProp="arrowFowd" clickFunc={() => {
            let buttonReq = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({"move" : "forward"})
            };
            
            fetch(window.location.href + "/manual", buttonReq)
        }}/>
        <NavButton id="robotDown" imgProp="arrowDown" clickFunc={() => {
            let buttonReq = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({"move" : "backward"})
            };
            
            fetch(window.location.href + "/manual", buttonReq)
        }}/>
        <NavButton id="robotCW" imgProp="arrowCW" clickFunc={() => {
            let buttonReq = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({"move" : "turnCW"})
            };
            
            fetch(window.location.href + "/manual", buttonReq)
        }}/>
        <NavButton id="robotCCW" imgProp="arrowCCW" clickFunc={() => {
            let buttonReq = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({"move" : "turnCCW"})
            };
            
            fetch(window.location.href + "/manual", buttonReq)
        }}/>
        <NavButton id="robotSample" imgProp="arrowSample" clickFunc={() => {
            let buttonReq = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({"move" : "sampler"})
            };
            
            fetch(window.location.href + "/manual", buttonReq)
        }}/>
    </View>
    </>);
}