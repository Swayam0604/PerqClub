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

// Form submission handling
document.addEventListener("DOMContentLoaded", function () {
  const contactForm = document.getElementById("contactForm");
  const formSubmitMessage = document.getElementById("formSubmitMessage");

  if (contactForm) {
    contactForm.addEventListener("submit", function (e) {
      e.preventDefault();

      // Simple form validation
      const name = document.getElementById("name").value;
      const email = document.getElementById("email").value;
      const message = document.getElementById("message").value;

      if (!name || !email || !message) {
        alert("Please fill in all required fields.");
        return;
      }

      // Simulate form submission (would be replaced with actual AJAX request)
      simulateFormSubmission();
    });
  }

  function simulateFormSubmission() {
    // Show loading state
    const submitBtn = contactForm.querySelector(".submit-btn");
    const originalBtnText = submitBtn.textContent;
    submitBtn.textContent = "Sending...";
    submitBtn.disabled = true;

    // Simulate server request delay
    setTimeout(function () {
      // Hide the form
      contactForm.style.display = "none";

      // Show success message
      formSubmitMessage.classList.remove("hidden");

      // Reset form for potential future use
      contactForm.reset();
      submitBtn.textContent = originalBtnText;
      submitBtn.disabled = false;

      // Auto scroll to the success message
      formSubmitMessage.scrollIntoView({ behavior: "smooth", block: "center" });
    }, 1500);
  }

  // Form input animation
  const formInputs = document.querySelectorAll(
    ".form-group input, .form-group textarea, .form-group select"
  );

  formInputs.forEach((input) => {
    // Add focus effect
    input.addEventListener("focus", function () {
      this.parentElement.classList.add("focused");
    });

    // Remove focus effect
    input.addEventListener("blur", function () {
      if (this.value === "") {
        this.parentElement.classList.remove("focused");
      }
    });

    // Check initial state (for browser autofill)
    if (input.value !== "") {
      input.parentElement.classList.add("focused");
    }
  });

  // Hours section animation
  const hoursSection = document.querySelector(".hours-section");
  const hoursEntries = document.querySelectorAll(
    ".hours-grid .day, .hours-grid .time"
  );

  // Add animation when hours section comes into view
  if (hoursSection) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            // Animate the entries with a staggered delay
            hoursEntries.forEach((el, index) => {
              setTimeout(() => {
                el.style.opacity = "1";
                el.style.transform = "translateY(0)";
              }, 100 * index);
            });

            // Unobserve after animation
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.3 }
    );

    observer.observe(hoursSection);

    // Set initial state for animation
    hoursEntries.forEach((el) => {
      el.style.opacity = "0";
      el.style.transform = "translateY(20px)";
      el.style.transition = "opacity 0.4s ease, transform 0.4s ease";
    });
  }
});



// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();

    const targetId = this.getAttribute("href");

    if (targetId === "#") return;

    const targetElement = document.querySelector(targetId);

    if (targetElement) {
      targetElement.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  });
});

// Add animation for contact cards
const contactCards = document.querySelectorAll(".contact-card");

// Simple animation on page load - modified to not interfere with hover
window.addEventListener("load", function () {
  setTimeout(() => {
    contactCards.forEach((card, index) => {
      // Set initial opacity to 0 for fade-in effect
      card.style.opacity = "0";

      setTimeout(() => {
        // Only animate opacity, not transform (which would interfere with hover)
        card.style.opacity = "1";
        // Don't set transform here, let CSS handle hover transform
      }, index * 200);
    });
  }, 300);
});
