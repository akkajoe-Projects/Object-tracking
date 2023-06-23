function opencvCheck() {
    document.getElementById('checker').innerHTML="OpenCV is ready!"
    var video = document.getElementById("video_feed")
    const canvas = document.getElementById("canvas")
    var ctx= canvas.getContext('2d')
    coords= document.getElementById("coords")

    function refreshCanvas() {
        ctx.drawImage(video, 0, 0, 720, 640)
    }
    //displays the mjpeg after an interval of 10ms
    window.setInterval(refreshCanvas, 50)  

    //to hold the mouse position
    let startX
    let startY
    var mouseX
    var mouseY
    var width
    var height
    var isDown= false
    var mouseUp

    // using pageX instead of clientX because of scroll offset
    $("canvas").on("mousedown", function(event) {
        startX = event.pageX - this.offsetLeft;
        startY = event.pageY - this.offsetTop;
        coords.innerHTML= `x val is ${startX} and y val is ${startY}`
        isDown= true
        mouseUp= true
    });  
    //mouseout refers to when the mouse moves out of an element
    canvas.addEventListener('mouseout',(e)=>{
        isDown= false
        mouseUp= true
    })
    $("canvas").on("mousemove", function(event) {
        if (isDown) {
        mouseX = event.pageX - this.offsetLeft;
        mouseY = event.pageY - this.offsetTop;
        width= mouseX-startX
        height=mouseY-startY
        mouseUp= false
    }});
    canvas.addEventListener('mouseup',(e)=>{
        isDown= false
        mouseUp=true
        sendData(startX,startY,width,height)
    })

    function drawRect(){
        if (!mouseUp){
            ctx.strokeStyle="green"
            ctx.lineWidth=2
            ctx.strokeRect(startX,startY,width,height)
        }       
    }
    setInterval(drawRect,50)

    function sendData(x1,y1,x2,y2){
       let data = {
        x:x1,
        y:y1,
        width:x2,
        heightt:y2
       }
        fetch('/initbb',{
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=UTF-8"},
        "body": JSON.stringify(data)
        }).then(res=> {
            if(res.ok){
                return res.json()
            }else{
                alert('smething is wrong')
            }
        }).then(json => {console.log(json)})
        .catch((err) => console.error(err))
    }   
}
