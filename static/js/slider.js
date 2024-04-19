  /*sliding script start-----------------------*/
  const sliderContainer = document.getElementById('slider-container');
  const imageList = document.getElementById('image-list');
  const sliderImages = document.querySelectorAll('.slider-image');
  const prevBtn = document.getElementById('prev-btn');
  const nextBtn = document.getElementById('next-btn');

  let currentIndex = 0;

  function nextSlide() {
    currentIndex = (currentIndex + 1) % sliderImages.length;
    updateSlider();
  }

  function prevSlide() {
    currentIndex = (currentIndex - 1 + sliderImages.length) % sliderImages.length;
    updateSlider();
  }

  function updateSlider() {
    const newPosition = -currentIndex * 100 + '%';
    imageList.style.transform = 'translateX(' + newPosition + ')';
  }

  setInterval(nextSlide, 3000); // Change slide every 3 seconds (adjust as needed)


