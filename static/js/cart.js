function addqty(productID,change){
      console.log(productID);
      var value = parseInt($('#inp-val-'+productID).val());
      value = value+1;
      console.log(value);
      var csrftoken = getCookie('csrftoken');
      cart(productID,csrftoken,value,change);
}

function rmvqty(productID,change){
      console.log(productID);
      var value = parseInt($('#inp-val-'+productID).val());
      value = value-1;
      console.log(value);
      var csrftoken = getCookie('csrftoken');
      cart(productID,csrftoken,value,change);
}

function cart(productID,csrftoken,value,change){
      console.log('working');
      $.ajax({
          type:'POST',
          url:'/update_cart/'+productID,
          data:{
              'qty':value,
              'csrfmiddlewaretoken': csrftoken,
          },
        success:function(response){
            
              if (change == 'cart'){
                $("#cart_reload").load(location.href + " #cart_reload>*", "")
                $("#cart_list").load(location.href + " #cart_list>*", "")
              }
            else if(change == 'checkout'){
                if(value<=0){
                    $('#product-'+productID).remove();
                }else{
                    $('#inp-val-'+productID).val(value);
                }
                console.log('checkout')
            }else if(change == 'productlist'){
                $("#cart-btn-"+productID).load(location.href + " #cart-btn-"+productID+">*", "")
                console.log('productlist')
            }else{
                console.log("not cart checkout");
            }
        },
          error: function (xhr, errmsg, err) {
              console.log(errmsg);
          }
    })
  
}

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