let time = 4000;
    imgNowIndex = 0;
    images = document.querySelectorAll("#slider img");
    max = images.length;

function proxImagem() {    
    images[imgNowIndex].classList.remove("selected");
    imgNowIndex ++;
    if (imgNowIndex >= max)
        imgNowIndex = 0;
    images[imgNowIndex].classList.add("selected")
}

function start() {
    setInterval(() => {
        proxImagem()
    }, time)       
}

window.addEventListener("load", start)
