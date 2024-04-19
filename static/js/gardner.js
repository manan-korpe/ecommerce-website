function cheackSlot(){
      var service = "{{service.id}}";
      var date = $("#dateInput").val();
      var slots = '{{slots|safe|escapejs}}';
      var jsondata = JSON.stringify(slots);

      document.getElementById("slot-time").value=null;
      var buttons = document.getElementsByClassName('formbold-form-input-slot');
      for (var i = 0; i < buttons.length; i++) {
          buttons[i].classList.remove('selected');
      }
      var button = document.querySelectorAll(".slot-btn");
      

      $.ajax({
            type:"GET",
            url:"/gardner/dateslot/",
            data:{
                  "service":service,
                  "date":date,
                  "slots":jsondata,
            },
            success:function(response){
                  not_avl = response.not_avl_slot;
                      
                      button.forEach(function(b) {
                          console.log(b);
                          b.setAttribute("onclick", "setTime(this)");
                          b.classList.remove('not-avl');
                      });
                      button.forEach(function(b) {
                        button_value = b.innerHTML;
                        not_avl.forEach(function(val){
                          if(button_value==val){
                            console.log(b);
                            b.removeAttribute("onclick");
                            b.classList.add('not-avl');
                          }                                                       
                        });
                      });
            },
            error: function(xhr, status, error) {
                  console.error(error);
            }
      });
  }
  function updateMinDate() {
    // Get today's date
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); // January is 0!
    var yyyy = today.getFullYear();

    today = yyyy + '-' + mm + '-' + dd;

    // Set the minimum date for the date input field to today
    document.getElementById("dateInput").min = today;
  }

// Call the function to set the initial minimum date
updateMinDate();
// Add event listener to update the minimum date whenever the input changes
document.getElementById("dateInput").addEventListener("change", updateMinDate);

function setTime(obj){
    var val = obj.innerHTML;
  document.getElementById("slot-time").value=val;

  var buttons = document.getElementsByClassName('formbold-form-input-slot');
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].classList.remove('selected');
    }
    
    // Add the 'selected' class to the clicked button
    obj.classList.add('selected');
}