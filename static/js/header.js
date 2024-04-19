      function myfunction(){
        document.getElementById("cat-items").classList.toggle("show");
        window.onclick = function(event){
          if(!event.target.matches('.cat-btn'))
          {
            var dropdowns=document.getElementsByClassName("cat-items");
            var i;
            for(i=0;i<dropdowns.length;i++)
            {
              var opendrop=dropdowns[i];
              if(opendrop.classList.contains('show'))
              {
                opendrop.classList.remove('show');
              }
            }
          }
        }
        console.log("js worked.")
      }

      

      