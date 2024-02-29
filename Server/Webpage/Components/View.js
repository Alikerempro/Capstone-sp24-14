export default  function View(props){
    return (<>
    <div className="container">
        {props.draggable == true ? <img src="../Images/dragBar.jpg"/> : <></>}
    </div>
    </>);
}