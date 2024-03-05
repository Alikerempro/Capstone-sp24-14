import View from "./View"

export default function CameraView(){
    return (<>
    <View dragable={true}>
        <div id="cameraStream">
            <img src="{{ url_for('camStream')}}"/>
        </div>
        <button id="enableStream"/>
        <button id="enableCV"/>
        <button id="savePicture"/>
    </View>
    </>);
}