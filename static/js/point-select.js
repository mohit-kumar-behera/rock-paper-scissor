const pointsBtn = [...document.getElementsByClassName("points-btn")];

function radioSelectPoint() {
    this.children[0].checked = true;
    for(i=0; i<pointsBtn.length; i++){
        pointsBtn[i].classList.remove("clicked");
    }
    this.classList.add("clicked");
}

pointsBtn.forEach(btn => {
    btn.addEventListener('click', radioSelectPoint);
})