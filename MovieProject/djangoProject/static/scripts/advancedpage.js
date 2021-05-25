let hidden_genre_input;
let chosesen_genres = [];

function click(item, genre_name) {
    // console.log("before:", item.style.display)
    if (item.style.display === "none" || item.style.display === '') {
        console.log("Clicked!", genre_name);
        chosesen_genres.push(genre_name);
        item.style.display = "inline";
    } else {
        const index = chosesen_genres.indexOf(genre_name);
        if (index > -1) {
            chosesen_genres.splice(index, 1);
        }
        item.style.display = "none";
    }
    console.log(chosesen_genres);
    hidden_genre_input.value = chosesen_genres;
}


window.onload = function () {
    console.log("Window loaded");
    let genre_items = document.getElementsByClassName("genre_wrapper");
    hidden_genre_input = document.getElementById("hidden genres");
    for (let i = 0; i < genre_items.length; i++) {
        let element = genre_items[i];
        let rectangle = element.querySelector(".rectangle");
        let actual_genre_name = element.querySelector(".genre_name").textContent;
        rectangle.onclick = function () {
            // console.log("Clicked element!");
            let svg = rectangle.getElementsByTagName("svg")[0];
            click(svg, actual_genre_name);
        };
    }

}