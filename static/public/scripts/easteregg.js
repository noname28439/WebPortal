
function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}


var SMILEYS = ["😀", "😁", "😂", "🤣", "😃", "😄", "😅", "😆", "😉", "😋", "😎", "😏", "😐", "🥱"]
function getFace(){
    let toReturn = SMILEYS[getRandomInt(SMILEYS.length)];
    console.log(toReturn);
    return toReturn;
}

function trigger_easteregg(remove){
    let i = 0;
    let itervalID = setInterval(function() {
        i++;
        spawn(remove)
        if(i>5)
            clearInterval(itervalID);
    }, 100)
}


function spawn(removeOnEnd){
    console.log("Triggered Easteregg...")
    let element = document.createElement("p");
    element.innerHTML=getFace()
    element.style = "position: fixed; font-size: 500%; left: -100px; top: -100px; z-index: 1; transform: rotate(90deg);"

    document.body.appendChild(element);


    var WIN_HEIGHT = window.innerHeight;
    var WIN_WIDTH = window.innerWidth;


    let x = WIN_WIDTH/2;
    let y = 10;
    let xspeed = getRandomInt(3)-1;
    let yspeed = getRandomInt(3)-1;
    let rotation = 180;

    var LIVETIME = 500+getRandomInt(200);
    let lived = 0;
    let rotationspeed = getRandomInt(5)+1;

    let itervalID = setInterval(function() {
        lived++;

        //falling speed
        if(y < WIN_HEIGHT-100)
            yspeed += 0.5;

        yspeed += (getRandomInt(3)-1)/10;
        xspeed += (getRandomInt(3)-1)/10;

        //Map borders
        if(y > WIN_HEIGHT){
            yspeed = -yspeed*0.95;
            y = WIN_HEIGHT-10;
        }
        if(x < 0 && xspeed < 0)
            xspeed = -xspeed;
        if(x+element.style.width > WIN_WIDTH && xspeed > 0)
            xspeed = -xspeed;

        //Set x and y position
        x += xspeed;
        y += yspeed;


        rotation+=rotationspeed;
        if(rotation>360){
            rotation = 0;
        }

        element.style.transform = "rotate("+rotation+"deg)";
        element.style.left = x+"px";
        element.style.top = y+"px";



        if(lived > LIVETIME){
            if(removeOnEnd)
                document.body.removeChild(element);
            clearInterval(itervalID);
        }
    }, 10)

}

//trigger_easteregg()