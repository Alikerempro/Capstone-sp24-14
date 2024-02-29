import View from "./View"

export default function CameraView(){
    return (<>
    <View dragable={true}>
        <div id="cameraStream"/>
        <button id="enableStream"/>
        <button id="enableCV"/>
        <button id="savePicture"/>
    </View>
    </>);
}