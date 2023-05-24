function opencvCheck() {
    document.getElementById('checker').innerHTML="OpenCV is ready!"
    const video = document.getElementById("video_feed")
    let cap=cv.imread(video)
    const canvas = document.getElementById("canvas")
    var ctx= canvas.getContext('2d')
    ctx.strokeStyle="green"
    ctx.lineWidth=2
    

    function refreshCanvas(x1=10,x2=30,x3=40,x4=40) {
        ctx.drawImage(video, 0, 0, 1000, 700)
    }

    //displays the mjpeg after an interval of 10ms
    window.setInterval(refreshCanvas, 10)  
    //calculate where the canvas in on the window
    //getBoundingClientReact() returns a DOMrect object providing info about the size of the element and its position relative to the viewport
    var canvasOffset = canvas.getBoundingClientRect()
    var offsetX= canvasOffset.left
    var offsetY= canvasOffset.top
    //to hold the mouse position
    var startX
    var startY
    var mouseX
    var mouseY
    var isDown= false
    var width
    var height
    console.log("WIDTH TYPE" + typeof(width))
    canvas.addEventListener('mousedown', (e) => {
        //preventDefault tells the user agent(web,browser) if the event is not explicitly handled, default action should not be taken
        e.preventDefault()
        e.stopPropagation()

        //To save the x and y val of the rectangle
        startX= parseInt(e.clientX - offsetX)
        startY =parseInt(e.clientY - offsetY)
        isDown= true
    })
    canvas.addEventListener('mouseup',(e)=>{
        e.preventDefault()
        e.stopPropagation()
        isDown= false
    })
    //mouseout refers to when the mouse moves out of an element
    canvas.addEventListener('mouseout',(e)=>{
        e.preventDefault()
        e.stopPropagation()
        isDown= false
    })
    canvas.addEventListener('mousemove',(e)=>{
        e.preventDefault()
        e.stopPropagation()
        
        if (isDown) { mouseX= parseInt(e.clientX-offsetX)
            mouseY= parseInt(e.clientY-offsetY)
    
            // ctx.clearRect(0,0,canvas.width,canvas.height)
    
            width= mouseX - startX
            height= mouseY - startY
            //draw a new rect from the start position to current mouse position
            console.log(startX,startY,width,height)
            sendData(startX,startY,width,height)
        } 
    })

    function sendData(x1,x2,y1,y2){
       let data = {
        "x":x1,
        "y":y1,
        "width":x2,
        "height":y2
       }
        fetch('/initbb',{
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(data)
        }).then(response=> {
            if(response.ok){
                return response.json()
            }else{
                alert('smething is wrong')
            }
        }).then(json => {console.log(json)})
        .catch((err) => console.error(err))

    }

    async function getRectCoords(){
        const response = await fetch('/initcoords')
        const responseJson = response.json()
        console.log('BLOB',responseJson)

    }

    getRectCoords().catch(error => {
        console.error(error)
    })
}


