export default function NavButton(props) {
    //Destination is at "Images/index.html.jpg" and "Images/settings.html.jpg"
    return (<>
            <input type="image" className="navButton" src={"Images/"+props.imgProp+".png"} onClick={props.clickFunc} ></input>
    </>);
}