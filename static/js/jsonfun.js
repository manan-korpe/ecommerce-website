

$('#quanity').on('click',function(){
    console.log("working ocut");
    var value = $(this).val();
    console.log(value);
    var productid = $('#product_id').val();
    console.log(productid);
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        type: 'POST',
        url:'/add_cart/'+productid,
        data:{
            'csrfmiddlewaretoken': csrftoken,
        },
        success: function (response) {
            $('#quanity').val(value);
            console.log(response);
        },
        error: function (xhr, errmsg, err) {
            console.log(errmsg);
        }
    })
});

$('.heart-icon').on('click', '.bx-heart, .bxs-heart', function() {
    var icon = $(this);
    var id = icon.data("product");
    var csrftoken = getCookie('csrftoken');

    $.ajax({
        type: 'POST',
        url: '/like/' + id,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        },
        dataType: 'json',
        success: function(response) {
            console.log("done");
            console.log(response.like);
            
            console.log(response.like.indexOf(id));
            // Toggle heart icon classes based on whether the product is liked or not
            if (response.like.indexOf(id) !== -1) {
                icon.removeClass('bx-heart').addClass('bxs-heart');
            } else {
                icon.removeClass('bxs-heart').addClass('bx-heart');
            }
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
});     
$('.add-to-cart-btn').on("click", function () {
    var productId = $(this).data('product-id');
    console.log('add to cart');
    console.log(productId);

    // Get the CSRF token from the cookie
    var csrftoken = getCookie('csrftoken');

    // Send the AJAX request
    $.ajax({
        type: 'POST',
        url: '/add_cart/' + productId,
        data: {
            'csrfmiddlewaretoken': csrftoken
        },
        success: function (response) {
            if(response.success){
                $("#reload"+productId).load(location.href + " #reload"+productId+">*", "");

                /*console.log("true");
                $('#msgadd').show();
                setTimeout(function(){
                    $('#msgadd').hide();
                },2000);*/
            }
            else{
                console.log("false")
                $('.out-stc').show();
                setTimeout(function(){
                    $('.out-stc').hide();
                },2000);
            }
            
            
        },
        error: function (xhr, errmsg, err) {
            console.log(errmsg);
        }
    });
});

$('.in-search').on('input',function(){
     val=$('.in-search').val().trim();
     $('.search-items').show();
     var csrftoken = getCookie('csrftoken');
     if (val.length > 0) {
        $.ajax({
            type: 'GET',
            url: '/search/',
            data: { 
                'query': val,
                'csrfmiddlewaretoken':csrftoken
            },
            success: function(response) {
                if(Object.keys(response.results1).length === 0 && Object.keys(response.results2).length === 0){
                    $('#search-items').hide();
        
                }else{
                    displayResults(response.results1,response.results2);
                }
                
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    } else {
        $('.search-items').hide();
        $('.search-items ul').empty();
    }

    function displayResults(results1,results2) {
        var resultHtml = '';
        var url='';
        results1.forEach(function(category) {
            url = '/productList/'+category.id;
            resultHtml += '<li class="search-contain"><a href="'+url+'">'+category.name+'</a></li>';
        });
        results2.forEach(function(product) {
            url = '/product/'+product.id;
            resultHtml += '<li class="search-contain"><a href="'+url+'">'+product.name+'</a></li>';
        });
        $('.search-items ul').html(resultHtml);
    }
 });
 $('.in-search').on('keypress', function(event) {
    if (event.which === 13) { // Check if Enter key was pressed
        event.preventDefault(); // Prevent default form submission behavior
        var firstResultLink = $('.search-items ul li:first-child a').attr('href');
        if (firstResultLink) {
            window.location.href = firstResultLink; // Navigate to the URL of the first search result
        }
    }
});
$('#search-button').on('click', function(event) {
    event.preventDefault(); // Prevent default form submission behavior
    var firstResultLink = $('.search-items ul li:first-child a').attr('href');
    if (firstResultLink) {
    window.location.href = firstResultLink; // Navigate to the URL of the first search result
    }
    
})

// Function to get the CSRF token from the cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}





