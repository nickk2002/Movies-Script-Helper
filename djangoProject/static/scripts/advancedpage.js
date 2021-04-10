function click(item) {
    // console.log("before:", item.style.display)
    if (item.style.display === "none" || item.style.display === '') {
        console.log("Clicked!");
        item.style.display = "inline";
    } else {
        item.style.display = "none";
    }
    // console.log("after:", item.style.display);
}


window.onload = function () {
    console.log("Window loaded");
    let genre_items = document.getElementsByClassName("rectangle");
    for (let i = 0; i < genre_items.length; i++) {
        let element = genre_items[i];
        console.log(element);
        element.onclick = function () {
            console.log("Clicked element!");
            let svg = element.getElementsByTagName("svg")[0];
            click(svg);
        };
    }

}