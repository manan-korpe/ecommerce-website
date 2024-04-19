document.querySelector('.add-sub').addEventListener('click', function() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
      
      const setError = (field, message) => {
            console.log("error genetate");
            document.getElementById(`${field}-error`).style.display = "block";
            const errorDisplay = document.getElementById(`${field}-error`);
            errorDisplay.innerText = message;
      }

      const setSuccess = (field) => {
            document.getElementById(`${field}-error`).style.display = "none";
            const errorDisplay = document.getElementById(`${field}-error`);
            errorDisplay.innerText = '';
      }

      function isValidIndianPhoneNumber(phoneNumber) {
            const regex = /^[7-9][0-9]{9}$/;
            return regex.test(phoneNumber);
      }
      function  check(value,field){
            if(value === '') {
                  setError(field, `${field} is required`);
            } else {
                  setSuccess(field);
            }
      }
      var sfname = document.getElementById('sfname').value;
      var slname = document.getElementById('slname').value;
      var sphone = document.getElementById('sphone').value;
      var saddress = document.getElementById('saddress').value;
      var slandmark = document.getElementById('slandmark').value;
      var scity = document.getElementById('scity').value;
      var spin = document.getElementById('spin_code').value;

      var newbtn = document.getElementById('new');
      var isnothidden = window.getComputedStyle(newbtn).display === "none";

      if (isnothidden){
             //shipping address
                  
            var name = sfname.trim();
            var lname = slname.trim();
            var phone = sphone.trim();
            var address = saddress.trim();
            var city = scity.trim();
            var pin = spin.trim();

            
            if(phone === '') {
                  setError('phone', 'phone is required');
            }
            else if (! isValidIndianPhoneNumber(phone)){
                  setError('phone', 'Enter valid phone number');
            } else {
                  setSuccess('phone');
            }

            check(name,'fname');
            check(lname,'lname');
            check(address,'address');
            check(city,'city');
            check(pin,'pin_code');
            
            sav = document.getElementById('shipping-value').value = 'new';
            console.log(sav);
      }

      var bfname = document.getElementById('bfname').value;
      var blname = document.getElementById('blname').value;
      var bphone = document.getElementById('bphone').value;
      var baddress = document.getElementById('baddress').value;
      var blandmark = document.getElementById('blandmark').value;
      var bcity = document.getElementById('bcity').value;
      var bpin = document.getElementById('bpin_code').value;

      var checkbox = document.getElementById('bill-check').checked;

      if (!checkbox){
      
            name = bfname.trim();
            lname = blname.trim();
            phone = bphone.trim();
            address = baddress.trim();
            city = bcity.trim();
            pin = bpin.trim();

            if(phone === '') {
                  setError('bphone', 'phone is required');
            }
            else if (! isValidIndianPhoneNumber(phone)){
                  setError('bphone', 'Enter valid phone number');
            } else {
                  setSuccess('bphone');
            }
            check(name,'bfname');
            check(lname,'blname');
            check(address,'baddress');
            check(city,'bcity');
            check(pin,'bpin_code');                       
      }
      
      var errors = document.querySelectorAll('.error');
      var hasErrors = false;
      var count = 0;
      errors.forEach(function(error) {

      var computedStyle = window.getComputedStyle(error);
      if (computedStyle.display === 'block') {
            hasErrors = true;
      }
      });

      console.log(hasErrors);

      if (!hasErrors){
            if(isnothidden){
                  var state = document.getElementById("sstate").value;
                  var shippping_address = saddress+","+scity+","+state+"-"+spin;
                  var div = document.getElementById('address-dispay');
                  div.innerHTML = "<i class='bx bx-user-circle'></i> "+sfname+" "+slname+"<br> <i class='bx bxs-phone'></i> "+sphone+"<br><br> <i class='fa-solid fa-location-dot'></i> "+shippping_address;
                  
                  if(checkbox){
                        var div = document.getElementById('biling-address');
                        div.innerHTML = "<i class='bx bx-user-circle'></i> "+sfname+" "+slname+"<br><i class='bx bxs-phone'></i> "+sphone+"<br><br><i class='fa-solid fa-location-dot'></i> "+shippping_address;
                  }

            }

            if(!checkbox){
                  var bstate = document.getElementById("bstate").value;
                  var div = document.getElementById('biling-address');
                  var billing_address = baddress+","+bcity+","+bstate+"-"+bpin;
                  div.innerHTML = "<i class='bx bx-user-circle'></i> "+bfname+" "+blname+"<br><i class='bx bxs-phone'></i> "+bphone+"<br><br><i class='fa-solid fa-location-dot'></i> "+billing_address;
            }

            document.getElementById('shiping-form-container').style.display = "none";
            document.getElementById('order-summery-container').style.display = "block";
            updateProgress(2);
      }
});


const progressItems = document.querySelectorAll('.progress li'); 
            
function updateProgress(step) {
      progressItems.forEach((item, index) => {
            if (index < step) {
            item.classList.add('active');
            } else {
            item.classList.remove('active');
            }
      });
}

document.querySelector('.sum-sub').addEventListener('click',function(){
      window.scrollTo({ top: 0, behavior: 'smooth' });
      document.getElementById('order-summery-container').style.display = "none";
      document.getElementById('pyment-form-container').style.display="block";
      console.log('working')
      updateProgress(3);
});
document.querySelectorAll('#edit-sum').forEach(button=>{
            button.addEventListener('click',function(){
            console.log('working');
            document.getElementById('shiping-form-container').style.display = "block";
            document.getElementById('order-summery-container').style.display = "none";
            updateProgress(1);

      });
});


var cod = document.getElementById('cod');

cod.addEventListener('click',function(even){
      even.preventDefault();

      cod.disabled = true;

      document.getElementById('order').submit();
});

/*-------------*/
