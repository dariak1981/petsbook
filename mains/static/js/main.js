
$(document).ready(function(){
  var productForm = $(".form-listing-ajax")

  productForm.submit(function(event){
    event.preventDefault();
    var thisForm = $(this);
    var actionEndpoint = thisForm.attr("action");
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();

    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function(data){
        var submitSpan = thisForm.find(".submit-span")
        if (data.added){
          submitSpan.html('<button type="submit" class="btn btn-link pl-0 text-white"><i class="fas fa-heart icon"></i></button>')
        }
        else {
          submitSpan.html('<button type="submit" class="btn btn-link pl-0 text-white"><i class="far fa-heart icon"></i></button>')
        }
        var navbarListingsCount = $(".navbar-listings-count")
        navbarListingsCount.text(data.cartListingsCount)
      },
      error: function(errorData){
        console.log("error")
        console.log(errorData)
      }
    })
  })
})

$(document).ready(function(){
  var productForm = $(".form-listing-ajax-home-page")

  productForm.submit(function(event){
    event.preventDefault();
    var thisForm = $(this);
    var actionEndpoint = thisForm.attr("action");
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();

    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function(data){
        var submitHomeSpan = thisForm.find(".submit-span-home-page")
        if (data.added){
          submitHomeSpan.html('<button type="submit" class="btn btn-link"><i class="fas fa-heart fa-lg icon"></i></button>')
        }
        else {
          submitHomeSpan.html('<button type="submit" class="btn btn-link"><i class="far fa-heart fa-lg icon"></i></button>')
        }
        var navbarListingsCount = $(".navbar-listings-count")
        navbarListingsCount.text(data.cartListingsCount)
      },
      error: function(errorData){
        console.log("error")
        console.log(errorData)
      }
    })
  })
})

$(document).ready(function(){
  var productForm = $(".form-listing-cart-ajax")

  productForm.submit(function(event){
    event.preventDefault();
    var thisForm = $(this);
    var actionEndpoint = thisForm.attr("action");
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();

    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function(data){
        var submitSpan = thisForm.find(".submit-span-cart")
        if (data.removed){
          submitSpan.html('<button type="submit" class="btn btn-link pl-0 text-dark">Удалено</button>')
        }
        else {
          submitSpan.html('<button type="submit" class="btn btn-link p-0" name="button"><i class="fas fa-times"></i></button>')
        }
        var navbarListingsCount = $(".navbar-listings-count")
        navbarListingsCount.text(data.cartListingsCount)
      },
      error: function(errorData){
        console.log("error")
        console.log(errorData)
      }
    })
  })
})



$(document).ready(function(){
  var productForm = $(".form-update-product-ajax")

  productForm.submit(function(event){
    event.preventDefault();
    var thisForm = $(this);
    var actionEndpoint = thisForm.attr("action");
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();

    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function(data){
        var submitSpan = thisForm.find(".submit-product-span")
        if (data.added){
          submitSpan.html('<button type="submit" class="btn btn-link"><i class="fas fa-heart icon"></i></button>')
        }
        else {
          submitSpan.html('<button type="submit" class="btn btn-link"><i class="far fa-heart icon"></i></button>')
        }
        var navbarProductsCount = $(".navbar-products-count")
        navbarProductsCount.text(data.cartProductsCount)
      },
      error: function(errorData){
        console.log("error")
        console.log(errorData)
      }
    })
  })
})


$(document).ready(function(){
  var productForm = $(".form-update-product-ajax-home-page")

  productForm.submit(function(event){
    event.preventDefault();
    var thisForm = $(this);
    var actionEndpoint = thisForm.attr("action");
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();

    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function(data){
        var submitSpan = thisForm.find(".submit-product-span-home-page")
        if (data.added){
          submitSpan.html('<button type="submit" class="btn btn-link"><i class="fas fa-heart fa-lg"></i></button>')
        }
        else {
          submitSpan.html('<button type="submit" class="btn btn-link"><i class="far fa-heart fa-lg"></i></button>')
        }
        var navbarProductsCount = $(".navbar-products-count")
        navbarProductsCount.text(data.cartProductsCount)
      },
      error: function(errorData){
        console.log("error")
        console.log(errorData)
      }
    })
  })
})






$(".carousel").carousel({
        interval: 6000,
        pause: "hover"
      });


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
