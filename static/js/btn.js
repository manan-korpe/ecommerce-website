
function newbtn(){
      var form = document.getElementById("order");
    /*  var elements = form.elements;

            for (var i = 0; i < elements.length; i++) {
            if (elements[i].type !== "button") {
                  elements[i].value = "";
            }
      }*/
      
      document.getElementById('shiping-form').style.display = "block";
      document.querySelector('#new').classList.toggle('hide');
      document.getElementById('cln').style.display = "block";
}

function editbtn(){
      document.getElementById('shiping-form').style.display = "block";
      document.querySelector('#new').classList.toggle('hide');
}

function clnbtn(){
      console.log("working");
      var div=document.querySelectorAll('.sstep');
      div.forEach(function(ediv){
            var errordiv = ediv.querySelector('.status');
            errordiv.style.display = "none";
      });

      sav = document.getElementById('shipping-value').value = ' ';
      console.log(sav)
      document.getElementById('cln').style.display = "none";
      document.getElementById('shiping-form').style.display = "none";
      document.querySelector('#new').classList.toggle('show');
    

}

document.querySelector('#bill-check').addEventListener('change',function(){
       
      if(this.checked){
            var div=document.querySelectorAll('.bstep');
            div.forEach(function(ediv){
                  var errordiv = ediv.querySelector('.status');
                  errordiv.style.display = "none";
            });
            sav = document.getElementById('billing-value').value = 'same';
            document.getElementById('billing-form').style.display = "none"; 
            
      }
      else{
            sav = document.getElementById('billing-value').value = '';
            document.getElementById('billing-form').style.display = "block";
      }
      console.log(sav)
});


