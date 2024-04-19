function finalurl(){
    var url = new URL(window.location.href);
    var search_params = url.searchParams;
    search_params.set('sort',document.getElementById("sort").value);
    url.search = search_params.toString();
    var new_url = url.toString();
    console.log(new_url);
    return new_url
}

// review container and submit form in product details page 

                function fillStars(clickedElement, index) {
                    var stars = document.querySelectorAll('.user-ratting i');

                    for (var i = 0; i <= index; i++) {
                        stars[i].classList.remove('bx-star');
                        stars[i].classList.add('bxs-star');
                    }

                    for (var i = index + 1; i < stars.length; i++) {
                        stars[i].classList.remove('bxs-star');
                        stars[i].classList.add('bx-star');
                    }
                    var ratingValue = index + 1;
                    document.getElementById('rattingvalue').value = ratingValue;
                }

                function formdisply(){
                    document.getElementById('rate-container').style.display = "block";
                }
                function closebtn(){
                    document.getElementById('rate-container').style.display = "none";
                }
                $(document).ready(function(){
                    $('#ratting-from').submit(function(e){
                        e.preventDefault();  // Prevent the form from submitting normally
                        
                        var formData = $(this).serialize();  // Serialize the form data
                        
                        $.ajax({
                            url: '/ratting/',  // URL to your Django view
                            type: 'POST',
                            data: formData,
                            success: function(response){
                                // Handle the success response
                                console.log(response);
                                $("#comment").load(location.href + " #comment"+">*", "");
                                $("#total-rating").load(location.href + " #total-rating"+">*", "");
                                
                            },
                            error: function(xhr, status, error){
                                // Handle errors
                                console.error(xhr.responseText);
                            }
                        });
                    });
                });

                function deleteratind(id){
                    $.ajax({
                            url: '/delete-ratting/'+id,  // URL to your Django view
                            type: 'GET',
                            success: function(response){
                                // Handle the success response
                                console.log("working");
                                $("#comment").load(location.href + " #comment"+">*", "");
                                $("#total-rating").load(location.href + " #total-rating"+">*", "");
                                
                            },
                            error: function(xhr, status, error){
                                // Handle errors
                                console.error(xhr.responseText);
                            }
                        });
                }



//multi image in product details page 
const allhoverimg = document.querySelectorAll('.hover-image div');
            const imagecontainer = document.querySelector('.img-container');

           // window.addEventListener('DOMContentLoaded', () => {
             //   allhoverimg[0].classList.add('active');
            //});

            allhoverimg.forEach((image) => {
                image.addEventListener('mouseover', () => {
                    imagecontainer.querySelector('img').src = image.querySelector('img').src;
                    resetactiveimg();
                    image.classList.add('active');
                });
            });

            function resetactiveimg() {
                allhoverimg.forEach((img) => {
                    img.classList.remove('active');
                });
            }
