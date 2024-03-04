import View from "./View"

export default function ControlView(){
    return (<>
    <View dragable={true}>
        <button id="robotPause"/>
        <button id="robotManual"/>
        <button id="robotUp"/>
        <button id="robotDown"/>
        <button id="robotCW"/>
        <button id="robotCCW"/>
        <button id="robotSample"/>
    </View>
    </>);
}