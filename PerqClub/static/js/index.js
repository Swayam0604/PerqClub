/* to make the toggle functioning */
function toggleMenu() {
  const menu = document.getElementById("mainNav"); // Fixed ID reference
  menu.classList.toggle("active");
}

document.addEventListener("DOMContentLoaded", function () {
  const menu = document.getElementById("mainNav");
  const menuItems = menu.querySelectorAll("a"); // Select all links inside the menu

  // Close menu when a menu item is clicked
  menuItems.forEach((item) => {
    item.addEventListener("click", function () {
      menu.classList.remove("active");
    });
  });

  const slides = document.querySelectorAll(".hero-slide");
  const indicators = document.querySelectorAll(".indicator");
  let currentSlide = 0;

  // Set initial active slide
  setActiveSlide(0);

  // Start auto rotation
  let slideInterval = setInterval(nextSlide, 4000); // Change to 4000ms for faster rotation

  // Pause auto rotation on hover
  slides.forEach((slide) => {
    slide.addEventListener("mouseover", function () {
      clearInterval(slideInterval);
    });
    slide.addEventListener("mouseout", function () {
      slideInterval = setInterval(nextSlide, 3000); // Restart auto rotation
    });
  });

  // Add click handlers to indicators
  indicators.forEach((indicator) => {
    indicator.addEventListener("click", function () {
      const slideIndex = parseInt(this.getAttribute("data-index"));
      setActiveSlide(slideIndex);

      // Reset the interval when manually changing slides
      clearInterval(slideInterval);
      slideInterval = setInterval(nextSlide, 5000);
    });
  });

  function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
    setActiveSlide(currentSlide);
  }

  function setActiveSlide(index) {
    // Remove active class from all slides and indicators
    slides.forEach((slide) => slide.classList.remove("active"));
    indicators.forEach((indicator) => indicator.classList.remove("active"));

    // Add active class to current slide and indicator
    slides[index].classList.add("active");
    indicators[index].classList.add("active");

    currentSlide = index;
  }
});

//* Cafe Slideshow Script */
// This script handles the functionality of the cafe slideshow, including image loading, navigation, and touch events.

document.addEventListener("DOMContentLoaded", function () {
  // Handle missing images with placeholders
  document.querySelectorAll(".slide").forEach((img) => {
    img.onerror = function () {
      this.src = "";
      this.alt = "Cafe placeholder image";
    };
  });

  // Select all slideshows
  const slideshows = document.querySelectorAll(".cafe-slideshow");

  // Initialize each slideshow
  slideshows.forEach((slideshow) => {
    const slides = slideshow.querySelectorAll(".slide");
    const dots = slideshow.querySelectorAll(".dot");
    const prevBtn = slideshow.querySelector(".prev-btn");
    const nextBtn = slideshow.querySelector(".next-btn");
    let currentIndex = 0;
    let slideInterval;

    // Function to show specific slide
    function showSlide(index) {
      // Remove active class from all slides and dots
      slides.forEach((slide) => slide.classList.remove("active"));
      dots.forEach((dot) => dot.classList.remove("active"));

      // Set active class to current slide and dot
      slides[index].classList.add("active");
      dots[index].classList.add("active");

      currentIndex = index;
    }

    // Function to show next slide
    function nextSlide() {
      const newIndex = (currentIndex + 1) % slides.length;
      showSlide(newIndex);
    }

    // Function to show previous slide
    function prevSlide() {
      const newIndex = (currentIndex - 1 + slides.length) % slides.length;
      showSlide(newIndex);
    }

    // Set up click events for dots
    dots.forEach((dot, index) => {
      dot.addEventListener("click", () => {
        showSlide(index);
        resetInterval();
      });
    });

    // Set up click events for next/prev buttons
    if (prevBtn) {
      prevBtn.addEventListener("click", () => {
        prevSlide();
        resetInterval();
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", () => {
        nextSlide();
        resetInterval();
      });
    }

    // Function to reset interval
    function resetInterval() {
      clearInterval(slideInterval);
      startInterval();
    }

    // Function to start automatic slideshow
    function startInterval() {
      slideInterval = setInterval(nextSlide, 4000); // Change slide every 4 seconds
    }

    // Start automatic slideshow
    startInterval();

    // Pause slideshow on hover
    slideshow.addEventListener("mouseenter", () => {
      clearInterval(slideInterval);
    });

    // Resume slideshow on mouse leave
    slideshow.addEventListener("mouseleave", () => {
      startInterval();
    });

    // Touch events for mobile
    let touchStartX = 0;
    let touchEndX = 0;

    slideshow.addEventListener(
      "touchstart",
      (e) => {
        touchStartX = e.changedTouches[0].screenX;
      },
      { passive: true }
    );

    slideshow.addEventListener(
      "touchend",
      (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
      },
      { passive: true }
    );

    function handleSwipe() {
      const minSwipeDistance = 50;
      if (touchEndX < touchStartX - minSwipeDistance) {
        // Swiped left, show next slide
        nextSlide();
        resetInterval();
      } else if (touchEndX > touchStartX + minSwipeDistance) {
        // Swiped right, show previous slide
        prevSlide();
        resetInterval();
      }
    }
  });
});
