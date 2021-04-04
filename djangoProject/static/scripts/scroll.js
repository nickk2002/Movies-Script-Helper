
let scrollDiv;
let cast;
let peopleArray;


function find_elements(){
    scrollDiv = document.getElementById("myscroll");
    cast = document.getElementById("cast");
    peopleArray = document.getElementsByClassName("person");
}
function calculate_cast_length(person_div,number_of_actors){
    let person_width = person_div.getBoundingClientRect().width;
    cast.style.width = person_width * number_of_actors + "px";
    console.log("Cast has now a width of ",cast.style.width,"to handle",number_of_actors);
}
function calculate_scroll_length(){
    scrollDiv.style.width = 0.2 * cast.getBoundingClientRect().width + "px";
}
Math.Clamp = function (value, min, max) {
    if (value < min) {
        return min;
    } else if (value > max) {
        return max;
    }

    return value;
};


function do_scroll() {



    let lastMouseX;
    let marginLeft = scrollDiv.offsetLeft;
    let maxWidth = cast.getBoundingClientRect().width - scrollDiv.getBoundingClientRect().width;

    console.log("max width", maxWidth);
    let currentLeft;
    let isDown = false;

    scrollDiv.addEventListener('mousedown', function (e) {
        isDown = true;
        lastMouseX = e.clientX;
        const rect = scrollDiv.getBoundingClientRect();
        currentLeft = rect.x - marginLeft;
        console.log("Margin Left", currentLeft);
    }, true);
    document.addEventListener('mouseup', function () {
        isDown = false;
    }, true);

    document.addEventListener('mousemove', function (e) {
        if (isDown) {
            let newLeftValue = (e.clientX - lastMouseX + currentLeft);
            newLeftValue = Math.Clamp(newLeftValue, 0, maxWidth);
            scrollDiv.style.left = newLeftValue + 'px';
            for(let i = 0; i < peopleArray.length; i++){
                let person = peopleArray[i];
                person.style.left= -newLeftValue + 'px';
            }
        }
    }, true);

}

window.onload = function () {
    console.log("on load called");
    find_elements();
    calculate_cast_length(peopleArray[0],4 );
    calculate_scroll_length();
    do_scroll();
}