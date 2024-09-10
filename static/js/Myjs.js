
function displayOverlay(className){
  var overlay = document.querySelector('.'+ className);
  overlay.style.display = 'block';
}

function hideOverlay(className){
  var overlay = document.querySelector('.'+ className);
  overlay.style.display = 'none';
}


function showList(className) {
  document.querySelector('.'+ className).style.display = 'block';
  
}

function closeList(className) {
  document.querySelector('.'+ className).style.display = 'none';
}

$('.dropdown-toggle').dropdown()

/*function displayOverlay() {
  var addFileElements = document.getElementsByClassName("addFile");
  if (addFileElements.length > 0) {
    addFileElements[0].style.display = 'flex';

    // Add a class to initiate the animation
    addFileElements[0].classList.add('moveInAnimation');
  }
}

function hideOverlay() {
  var addFileElements = document.getElementsByClassName('addFile');
  if (addFileElements.length > 0) {
    // Remove the class to initiate the animation in reverse
    addFileElements[0].classList.remove('moveInAnimation');

    // Wait for the animation to complete and then hide the element
    setTimeout(function () {
      addFileElements[0].style.display = 'none';
    }, 300); // Adjust the time to match your CSS transition duration
  }
}

.moveInAnimation {
  animation: moveInFromLeft 0.3s ease-in-out;
}

@keyframes moveInFromLeft {
  from {
    transform: translateX(-100%);
  }
  to {
    transform: translateX(0);
  }
}



*/
