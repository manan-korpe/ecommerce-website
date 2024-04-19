
  document.getElementById('editprofileButton').addEventListener('click', function(){

    console.log("working.....");
    document.getElementById("editprofileButton").style.display = 'none';
    document.getElementById("submitprofileButton").style.display = 'block';

    var inputs = document.querySelectorAll('.info-input input');
    inputs.forEach(function(input) {
    input.removeAttribute('readonly');
   });
  });

//
      $('#editButton').on('click',function(){
                $('.update-address').show();
                $('.e-d-btn').hide();
      })

      function deleteaddress(addressId){
        var csrftoken = getCookie('csrftoken');
        console.log("working")
        
        $.ajax({
          type:'POST',
          url:'/delete_address/'+addressId,
          data:{
            'csrfmiddlewaretoken':csrftoken,
          },
          success:function(response){
            
            console.log(response);
            $("#address").load(location.href + " #address>*", "")
          },
          error:function(xhr,status,error){
          console.log(error);
          }
        });
      }

      function closebtn(){
            document.getElementById('pic').style.display = "none";
        }
        function showpicform(){
          document.getElementById('pic').style.display = "block";
        }

        $('#btn-new').on('click',function(){
            $('#empty-form').show();
            $('#btn-new').hide();
        })  

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
