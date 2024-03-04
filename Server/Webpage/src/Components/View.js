export default  function View(props){
    return (<>
    <div className="comboContainer">
        {props.dragable == true ? <img className="dragBar" id={"dragger_"+props.name} src="../Images/dragBar.jpg"/> : null}
        <div className="container" id={"container_"+props.name}>
            {props.children}
        </div>
    </div>
    </>);
}