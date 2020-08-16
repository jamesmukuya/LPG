// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
//var btn = document.getElementById("myBtn");

// Get the element that closes the modal
var close = document.getElementById("closeModal");

// When the window loads, open the modal
window.onload = function () {
  modal.style.display = "flex";
}

// When the user clicks on <span> (x), close the modal
close.onclick = function () {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}