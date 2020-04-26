
$('.pop').each(function () {
    var $elem = $(this);
    $elem.popover({
        placement: 'right',
        trigger: 'hover',
        html: true,
        container: $elem
    });
});


function previewImage(event) {
    var reader = new FileReader();
    var imageField = document.getElementById("image-field-0")

    reader.onload = function() {
      if(reader.readyState == 2) {
        imageField.src = reader.result;
      }
    }
    reader.readAsDataURL(event.target.files[0]);
}


function previewImage1(event) {
    var reader = new FileReader();
    var imageField = document.getElementById("image-field-1")

    reader.onload = function() {
      if(reader.readyState == 2) {
        imageField.src = reader.result;
      }
    }
    reader.readAsDataURL(event.target.files[0]);
}


function previewImage2(event) {
    var reader = new FileReader();
    var imageField = document.getElementById("image-field-2")

    reader.onload = function() {
      if(reader.readyState == 2) {
        imageField.src = reader.result;
      }
    }
    reader.readAsDataURL(event.target.files[0]);
}


function previewImage3(event) {
    var reader = new FileReader();
    var imageField = document.getElementById("image-field-3")

    reader.onload = function() {
      if(reader.readyState == 2) {
        imageField.src = reader.result;
      }
    }
    reader.readAsDataURL(event.target.files[0]);
}



function previewImage4(event) {
    var reader = new FileReader();
    var imageField = document.getElementById("image-field-4")

    reader.onload = function() {
      if(reader.readyState == 2) {
        imageField.src = reader.result;
      }
    }
    reader.readAsDataURL(event.target.files[0]);
}



$(document).ready(function(){
    $(".GaugeMeter").gaugeMeter();
  });

let start // set on the first step to the timestamp provided
const el = document.getElementById('number') // get the element
const final = parseInt(el.textContent, 10) // parse out the final number
const duration = 2000 // duration in ms
const step = ts => {
  if (!start) {
    start = ts
  }
  // get the time passed as a fraction of total duration
  let progress = (ts - start) / duration

  el.textContent = Math.floor(progress * final) // set the text
  if (progress < 1) {
    // if we're not 100% complete, request another animation frame
    requestAnimationFrame(step)
  }
}
// start the animation
requestAnimationFrame(step)
