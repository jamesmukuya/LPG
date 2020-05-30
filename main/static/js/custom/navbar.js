
const navSlide =() =>{
  const burger = document.querySelector('.burger');
  const nav = document.querySelector('.nav-links');

	burger.addEventListener('click',()=>{
		nav.classList.toggle('nav-active');
	})
}
navSlide();

// when user clicks outside the Nav
const body = document.getElementById('bodyDiv');
body.addEventListener('click', function (e) {
  if (e.target.className.includes('nav-active')){
    console.log('clicked nav div');
  }
  let nav_list = document.querySelector('.nav-links');
  nav_list.classList.remove('nav-active');
})
/*
var btnContainer = document.getElementById("btnDiv");

// Get all buttons with class="btn" inside the container
var btns = btnContainer.getElementsByClassName("btn");

// Loop through the buttons and add the active class to the current/clicked button
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("btn active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
  });
}
*/
