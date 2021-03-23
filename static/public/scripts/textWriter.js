

var toRewriteList = document.getElementsByClassName("retype")

for(let i = 0; i<toRewriteList.length; i++){
    currentElement = toRewriteList[i]
    //console.log("retype: "+currentElement);
    rewrite(currentElement);
}

function rewrite(element){
    let content = element.innerHTML;
    
    element.innerHTML = "*";
    let i = -10;
    let animationContent = "";
    let itervalID = setInterval(function() {
        if(i >= 0){
            animationContent += content.split("")[i];
            element.innerHTML = animationContent;
            if(i>content.length-2)
                clearInterval(itervalID);
        }
        i+=1
        }, 100)
}



