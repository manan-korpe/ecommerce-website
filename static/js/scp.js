function cgnp(req,res){
      var selectedcity = $(req).val();
      $.ajax({
      url: "/get_pin/",
      type: "GET",
      data: { city_id : selectedcity },
      success: function(data) {
            console.log(data);
            var cd = $(res);
            console.log(cd);
            $(res).empty();
            $(res).append('<option value="" selected>Pincode</option>');
            $.each(data, function(key, value) {
                  $(res).append('<option value="' + value + '">' + value + '</option>');
            });
      }
      });
}
function cgnc(req,res){
      var selectedstate = $(req).val();
      $.ajax({
      url: "/get_cities/",
      type: "GET",
      data: { state_id : selectedstate },
      success: function(data) {
            console.log(data);
            var cd = $(res);
            console.log(cd);
            $(res).empty();
            $(res).append('<option value="" selected>City</option>');
            $.each(data, function(key, value) {
                  $(res).append('<option value="' + value + '">' + value + '</option>');
            });
      }
      });
}