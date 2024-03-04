export default function NavButton(props) {
    //Destination is at "Images/index.html.jpg" and "Images/settings.html.jpg"
    return (<>
        <a href={props.href}>
            <img id="navButton" src={"Images/"+props.href+".png"}></img>
        </a>
    </>);
}