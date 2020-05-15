$(document).ready(function(){

    //contact form handler
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action")
    
    function displaySubmitting(submitBtn, defaultText, doSubmit){
        if (doSubmit){
            submitBtn.addClass('disabled')
            submitBtn.html("<i class='fas fa-spin fa-spinner'></i>Submitting...")
        } else {
            submitBtn.removeClass('disabled')
            submitBtn.html(defaultText)
        }
        
    }

    contactForm.submit(function(event){
        event.preventDefault()

        var contactFormSubmitBtn = contactForm.find("[type='submit']")
        var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()

        var contactFormData = contactForm.serialize()
        var thisForm = $(this)
        displaySubmitting(contactFormSubmitBtn, "" ,true)
        $.ajax({
            method: contactFormMethod,
            url: contactFormEndpoint,
            data: contactFormData,
            success: function(data){
                thisForm[0].reset()
                $.alert({
                    title: "Your enquiry has been recorded",
                    content: data.message,
                    theme: "modern"
                })
                setTimeout(function(){
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt ,false)
                }, 500)
            },
            error: function(error){
                var jsonData = error.responseJSON
                var msg = ""

                $.each(jsonData, function(key, value){
                    msg += key +": " + value[0].message +"<br />"
                })

                $.alert({
                    title: "Oopps!",
                    content: msg,
                    theme: "modern"
                })
                setTimeout(function(){
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt ,false)
                }, 500)
            }
        })
    })
    // Auto Search
    var searchForm = $(".search-form")
    var searchInput = searchForm.find("[name='q']")
    var typingTimer;
    var typingInterval = 1500
    var searchBtn = searchForm.find('[type="submit"]')
    
    searchInput.keyup(function(event){
        //key released
        clearTimeout(typingTimer)
        typingTimer = setTimeout(performSearch, typingInterval)
    })
    searchInput.keydown(function(event){
        //key pressed
        clearTimeout(typingTimer)
        
        })
    
    function displaySearching(){
        searchBtn.addClass('disabled')
        searchBtn.html("<i class='fas fa-spin fa-spinner'></i>Searching...")
    }

    function performSearch(){
        displaySearching()
        var query = searchInput.val()
        window.location.href='/search/?q=' + query
    }


    // Cart + Add Courses
    var courseForm = $(".form-course-ajax")

    courseForm.submit(function(event){
        event.preventDefault();
        var thisForm = $(this)
        var actionEndpoint = thisForm.attr("data-endpoint") ;
        var httpMethod = thisForm.attr("method") ;
        var formData = thisForm.serialize();

        $.ajax({
            url: actionEndpoint,
            method: httpMethod,
            data: formData,
            success: function(data){
                var submitSpan = thisForm.find(".submit-span")
                if (data.added){
                    submitSpan.html('<button type="submit" class="btn btn-danger"><i class="fas fa-minus-hexagon"></i>Remove</button>')
                }
                else{
                    submitSpan.html('<button type="submit" class="btn btn-danger"> <i class="fas fa-shopping-cart"></i> Add to cart </button>')
                }
                var navbarCount = $(".navbar-cart-count")
                navbarCount.text(data.cartItemCount)
                var currentPath = window.location.href 
                if (currentPath.indexOf("cart") != -1){
                    refreshCart()
                }
            },
            error: function(errorData){
                $.alert({
                    title: "Oopps!",
                    content:"An error occured",
                    theme: "modern"
                    })
            }
        })


    })

    function refreshCart(){
        console.log("in current cart")
        var cartTable = $(".cart-table")
        var cartBody  = cartTable.find(".cart-body")
        var courseRows = cartBody.find(".cart-course")    
        var currentUrl = window.location.href                

        var refreshCartUrl = '/api/cart/'
        var refreshCartMethod = "GET";
        var data = {};
        $.ajax({
            url: refreshCartUrl,
            method:refreshCartMethod,
            data:data,
            success: function(data){
                var hiddenCartItemRemoveForm = $(".cart-items-remove-form")
                if (data.courses.length > 0 ){
                    courseRows.html(" ")
                    i = data.courses.length
                    $.each(data.courses, function(index, value){
                        var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                        newCartItemRemove.css("display", "block")
                        newCartItemRemove.find(".cart-item-course-id").val(value.id)
                        cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='"+ value.url + "'>" + value.name + "</a>" + newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>")
                        i --
                    })
                    cartBody.find(".cart-subtotal").text(data.subtotal)
                    cartBody.find(".cart-total").text(data.total)
                } else {
                    window.location.href = currentUrl
                }            
            },
            error: function(errorData){
                $.alert({
                    title: "Oopps!",
                    content:"An error occured",
                    theme: "modern"
                    })
            }
        })
    }

})