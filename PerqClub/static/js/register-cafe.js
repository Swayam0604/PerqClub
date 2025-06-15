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

// document.addEventListener("DOMContentLoaded", function () {
//   const sectionHeaders = document.querySelectorAll(
//     ".form-section .section-header"
//   );

//   sectionHeaders.forEach((header) => {
//     header.addEventListener("click", function () {
//       const formGrid = this.nextElementSibling; // Get the next sibling, which is the .form-grid

//       // Toggle the 'active' class on the header and the form grid
//       this.classList.toggle("active");
//       formGrid.classList.toggle("active");

//       // Optional: Close other open sections when one is opened
//       sectionHeaders.forEach((otherHeader) => {
//         if (otherHeader !== this && otherHeader.classList.contains("active")) {
//           otherHeader.classList.remove("active");
//           otherHeader.nextElementSibling.classList.remove("active");
//         }
//       });
//     });
//   });
// });


//  
// 
// static/js/register-cafe.js

document.addEventListener('DOMContentLoaded', function() {
  const sectionHeaders = document.querySelectorAll('.form-section .section-header');

  sectionHeaders.forEach(header => {
      header.addEventListener('click', function() {
          const formSection = this.closest('.form-section');
          const formGrid = formSection.querySelector('.form-grid');

          // Toggle active class on header and grid
          this.classList.toggle('active');
          formGrid.classList.toggle('active');
      });
  });

});