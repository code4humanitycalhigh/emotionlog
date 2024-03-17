function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("modal-opener");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

document.addEventListener('keydown', function(event){
    if(event.key == 'Enter'){
        sleep(500).then(() => { modal.style.display = "none"; });   
    }
})

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}