
var velocity = 0.2;

function update(){
    var pos = $(window).scrollTop();
    console.log(pos)
    document.body.style.backgroundPositionY = -(pos/2).toString()+"px";
    console.log("Pos: "+document.body.style.backgroundPositionX)
};

$(window).bind('scroll', update);
