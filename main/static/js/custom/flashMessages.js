// hide the flash messages

// get the flash element and close buttons
//const flashMessage = document.querySelector('.flash-message');
const flashMessage = document.getElementById('flashMessageOther');
const closeFlashBtn = document.querySelectorAll('.close-flash-message');

// add event listener to the buttons
for (btn of closeFlashBtn) {
  btn.addEventListener('click', function () {
    // close the flash div by adding inactive class
    flashMessage.classList.add('inactive');
  })
}