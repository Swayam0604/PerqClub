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

// Wait for the DOM to fully load
document.addEventListener("DOMContentLoaded", function () {
  // Get carousel elements
  const carousel = document.querySelector(".carousel");
  const slides = document.querySelectorAll(".carousel-slide");
  const dots = document.querySelectorAll(".dot");
  const prevBtn = document.querySelector(".prev-btn");
  const nextBtn = document.querySelector(".next-btn");

  // Set up initial state
  let currentSlide = 0;
  const totalSlides = slides.length;

  // Set initial position of slides
  updateCarouselPosition();

  // Set up automatic rotation
  let autoRotateInterval = setInterval(nextSlide, 3000); // Change slide every 5 seconds

  // Function to update carousel position
  function updateCarouselPosition() {
    // Move carousel to show current slide
    carousel.style.transform = `translateX(-${currentSlide * 100}%)`;

    // Update active dot
    dots.forEach((dot, index) => {
      dot.classList.toggle("active", index === currentSlide);
    });
  }

  // Function to go to next slide
  function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    updateCarouselPosition();
  }

  // Function to go to previous slide
  function prevSlide() {
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    updateCarouselPosition();
  }

  // Add event listeners to buttons
  nextBtn.addEventListener("click", function () {
    // Clear the automatic rotation and start a new one
    clearInterval(autoRotateInterval);
    nextSlide();
    autoRotateInterval = setInterval(nextSlide, 5000);
  });

  prevBtn.addEventListener("click", function () {
    // Clear the automatic rotation and start a new one
    clearInterval(autoRotateInterval);
    prevSlide();
    autoRotateInterval = setInterval(nextSlide, 5000);
  });

  // Add event listeners to dots
  dots.forEach((dot, index) => {
    dot.addEventListener("click", function () {
      // Clear the automatic rotation and start a new one
      clearInterval(autoRotateInterval);

      // Go to the clicked dot's corresponding slide
      currentSlide = index;
      updateCarouselPosition();

      autoRotateInterval = setInterval(nextSlide, 5000);
    });
  });

  // Pause auto-rotation when user hovers over carousel
  carousel.addEventListener("mouseenter", function () {
    clearInterval(autoRotateInterval);
  });

  // Resume auto-rotation when user's mouse leaves carousel
  carousel.addEventListener("mouseleave", function () {
    autoRotateInterval = setInterval(nextSlide, 5000);
  });
});


const highlightIcons = {
  "Free WiFi": "fa-wifi",
  "Power Outlets": "fa-plug",
  'Breakfast': "fa-utensils",
  'Parking': "fa-parking",
  "Work Friendly": "fa-laptop",
  "Pet Friendly": "fa-dog",
  "Vegan Options": "fa-leaf",
  "Outdoor Seating": "fa-chair",
  "Air Conditioning": "fa-snowflake",
};

document.addEventListener("DOMContentLoaded", function () {
  // Get cafe ID from URL parameter
  const urlParams = new URLSearchParams(window.location.search);
  const cafeId = urlParams.get("id") || "1"; // Default to cafe 1 if no ID provided

  // Load cafe data
  const cafe = cafeData[cafeId];
  if (!cafe) {
    console.error("Cafe not found!");
    return;
  }

  // Update page title
  document.title = `${cafe.name} - Details`;

  // Update cafe name
  document.querySelector(".cafe-info h1").textContent = cafe.name;

  // Update rating
  document.querySelector(
    ".cafe-rating span"
  ).textContent = `${cafe.rating} (${cafe.reviewCount} reviews)`;

  // Update location
  document.querySelector(".cafe-location span").textContent = cafe.location;

  // Update description
  const descriptionParagraphs = cafe.description.split("\n\n");
  const descriptionHTML = descriptionParagraphs
    .map((p) => `<p>${p}</p>`)
    .join("");
  document.querySelector(".cafe-description").innerHTML = descriptionHTML;

  const highlightsList = document.getElementById("highlights-list");
  highlightsList.innerHTML = ""; // Clear previous highlights

  cafe.highlights.forEach((highlight) => {
    const iconClass = highlightIcons[highlight] || "fa-star"; // fallback icon
    const div = document.createElement("div");
    div.className = "highlight-item";
    div.innerHTML = `<i class="fas ${iconClass}"></i> ${highlight}`;
    highlightsList.appendChild(div);
  });

  // Update map iframe
  document.querySelector(".map-container iframe").src = cafe.mapUrl;

  // Use the cafeId from URL parameters instead of hardcoding "1"
  updateReviews(cafeId);

  // Update carousel images
  const carouselSlides = document.querySelectorAll(".carousel-slide");
  cafe.images.forEach((imgSrc, index) => {
    if (carouselSlides[index]) {
      carouselSlides[index].querySelector("img").src = imgSrc;
    }
  });

  // Render nearby cafes
  renderNearbyCafes(cafe);

  // Initialize your existing carousel functionality
  initCarousel();
});

// The click event listeners for cafe-nav-item are a bit confusing here
// since they're not tied to specific cafe links on the page
// If these are meant for navigation between cafes on the same page,
// you might want to adjust this logic

function updateReviews(cafeId) {
  // Get the cafe data based on the provided ID
  const cafe = cafeData[cafeId];

  if (!cafe || !cafe.reviews) {
    console.error("Cafe data or reviews not found for ID:", cafeId);
    return;
  }

  // Get the container where reviews will be displayed
  const reviewsContainer = document.querySelector(".reviews-container");

  // Clear existing reviews
  reviewsContainer.innerHTML = "";

  // Loop through the reviews and create review cards
  cafe.reviews.forEach((review) => {
    // Create the review card HTML
    const reviewCard = document.createElement("div");
    reviewCard.className = "review-card";

    // Convert rating to stars
    const fullStars = Math.floor(review.rating);
    const halfStar = review.rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);

    let starsHTML = "";
    for (let i = 0; i < fullStars; i++) {
      starsHTML += '<i class="fas fa-star"></i>';
    }
    if (halfStar) {
      starsHTML += '<i class="fas fa-star-half-alt"></i>';
    }
    for (let i = 0; i < emptyStars; i++) {
      starsHTML += '<i class="far fa-star"></i>';
    }

    // Set the inner HTML of the review card
    reviewCard.innerHTML = `
        <div class="review-header">
          <div class="reviewer-img">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--!Font Awesome Free 6.7.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2025 Fonticons, Inc.--><path fill="#7d4f2a" d="M406.5 399.6C387.4 352.9 341.5 320 288 320l-64 0c-53.5 0-99.4 32.9-118.5 79.6C69.9 362.2 48 311.7 48 256C48 141.1 141.1 48 256 48s208 93.1 208 208c0 55.7-21.9 106.2-57.5 143.6zm-40.1 32.7C334.4 452.4 296.6 464 256 464s-78.4-11.6-110.5-31.7c7.3-36.7 39.7-64.3 78.5-64.3l64 0c38.8 0 71.2 27.6 78.5 64.3zM256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zm0-272a40 40 0 1 1 0-80 40 40 0 1 1 0 80zm-88-40a88 88 0 1 0 176 0 88 88 0 1 0 -176 0z"/></svg>
          </div>
          <div class="reviewer-info">
            <h4>${review.name}</h4>
            <div class="review-date">${review.date}</div>
          </div>
        </div>
        <div class="review-rating">
          ${starsHTML}
        </div>
        <p class="review-text">${review.text}</p>
        <div class="review-actions">
          <button class="helpful-btn">
            <i class="far fa-thumbs-up"></i> Helpful (${review.helpfulCount})
          </button>
          <button class="helpful-btn">
            <i class="far fa-comment"></i> Reply
          </button>
        </div>
      `;

    // Add the review card to the container
    reviewsContainer.appendChild(reviewCard);
  });
}

// Function to render nearby cafes
function renderNearbyCafes(cafe) {
  const cafesContainer = document.querySelector(".cafes-container");
  cafesContainer.innerHTML = ""; // Clear existing cafes

  // Check if the cafe has nearby cafes data
  if (!cafe.nearbyCafes || cafe.nearbyCafes.length === 0) {
    cafesContainer.innerHTML = "<p>No nearby cafes found.</p>";
    return;
  }

  // Process each nearby cafe
  cafe.nearbyCafes.forEach((nearbyCafeEntry) => {
    let nearbyCafeData;
    let nearbyCafeId;
    let shortDescription;
    let distance = "Nearby";

    // Check if nearbyCafe is an ID or an object
    if (
      typeof nearbyCafeEntry === "number" ||
      typeof nearbyCafeEntry === "string"
    ) {
      // It's an ID, get the full cafe data from cafeData
      nearbyCafeId = nearbyCafeEntry;
      nearbyCafeData = cafeData[nearbyCafeId];
      if (!nearbyCafeData) return; // Skip if ID doesn't exist

      // Use first paragraph of the main description as fallback
      shortDescription = nearbyCafeData.description.split("\n\n")[0];
    } else if (typeof nearbyCafeEntry === "object") {
      // It's an object with cafe data
      if (nearbyCafeEntry.id && cafeData[nearbyCafeEntry.id]) {
        // Reference to existing cafe
        nearbyCafeId = nearbyCafeEntry.id;
        nearbyCafeData = cafeData[nearbyCafeId];

        // Use custom shortDescription if provided, otherwise fallback
        shortDescription =
          nearbyCafeEntry.shortDescription ||
          nearbyCafeData.description.split("\n\n")[0];

        // Use custom distance if provided
        if (nearbyCafeEntry.distance) {
          distance = nearbyCafeEntry.distance;
        }
      } else {
        // Standalone cafe object (not in cafeData)
        nearbyCafeData = nearbyCafeEntry;
        nearbyCafeId = nearbyCafeEntry.id || "custom";
        shortDescription =
          nearbyCafeEntry.shortDescription ||
          nearbyCafeEntry.description.split("\n\n")[0];
        if (nearbyCafeEntry.distance) {
          distance = nearbyCafeEntry.distance;
        }
      }
    } else {
      return; // Skip invalid data
    }

    // Create the detail page URL
    const detailPageUrl = `cafedetails.html?id=${nearbyCafeId}`;

    // Create cafe card - now with clickable class
    const cafeCard = document.createElement("div");
    cafeCard.className = "cafe-card cafe-card-clickable";
    cafeCard.setAttribute("data-cafe-id", nearbyCafeId);

    // Create image slideshow HTML
    let slideshowHtml = "";
    if (nearbyCafeData.images && nearbyCafeData.images.length > 0) {
      slideshowHtml = `
          <div class="cafe-card-slideshow">
            <div class="slideshow-container">
              <div class="slides">
        `;

      // Add up to 3 images
      const imagesToShow = nearbyCafeData.images.slice(0, 3);

      imagesToShow.forEach((img, index) => {
        slideshowHtml += `
            <div class="slide ${index === 0 ? "active" : ""}">
              <img src="${img}" alt="${nearbyCafeData.name} - Image ${
          index + 1
        }">
            </div>
          `;
      });

      slideshowHtml += `
              </div>
              <button class="prev-btn">❮</button>
              <button class="next-btn">❯</button>
            </div>
          </div>
        `;
    } else {
      // Fallback if no images
      slideshowHtml = `
          <div class="cafe-card-img">
            <img src="" alt="${nearbyCafeData.name}">
          </div>
        `;
    }

    cafeCard.innerHTML = `
        ${slideshowHtml}
        <div class="cafe-card-content">
          <h3 class="cafe-card-title">
            <a href="${detailPageUrl}" class="cafe-title-link">${nearbyCafeData.name}</a>
          </h3>
          <div class="cafe-card-meta">
            <div class="cafe-card-rating">
              <i class="fas fa-star"></i>
              <span>${nearbyCafeData.rating}</span>
            </div>
            <div class="cafe-card-distance">${distance}</div>
          </div>
          <div class="cafe-card-location">
            <i class="fas fa-map-marker-alt"></i>
            <span>${nearbyCafeData.location}</span>
          </div>
          <p class="cafe-card-description">${shortDescription}</p>
          <a href="${detailPageUrl}" class="btn btn-primary btn-full">View Café</a>
        </div>
      `;

    cafesContainer.appendChild(cafeCard);

    // Initialize slideshow for this cafe card
    initCafeCardSlideshow(cafeCard);

    // Make the entire card clickable (except buttons and links)
    initClickableCard(cafeCard, detailPageUrl);
  });
}

// Function to make the card clickable
function initClickableCard(cardElement, url) {
  cardElement.addEventListener("click", function (e) {
    // Don't navigate if the user clicked on a button, link, or is dragging/selecting
    if (
      e.target.tagName === "BUTTON" ||
      e.target.tagName === "A" ||
      e.target.closest("button") ||
      e.target.closest("a") ||
      window.getSelection().toString()
    ) {
      return;
    }

    // Navigate to the cafe detail page
    window.location.href = url;
  });

  // Add hover cursor to indicate clickability
  cardElement.style.cursor = "pointer";
}

// Function to initialize slideshow for each cafe card
function initCafeCardSlideshow(cafeCard) {
  const slideshowContainer = cafeCard.querySelector(".slideshow-container");
  if (!slideshowContainer) return;

  const slides = cafeCard.querySelectorAll(".slide");
  const prevBtn = cafeCard.querySelector(".prev-btn");
  const nextBtn = cafeCard.querySelector(".next-btn");

  let currentSlideIndex = 0;
  let slideInterval;
  const autoRotateInterval = 4000; // Auto-rotate every 5 seconds

  // Function to show a specific slide
  function showSlide(index) {
    // Hide all slides
    slides.forEach((slide) => {
      slide.classList.remove("active");
    });

    // Show the selected slide
    slides[index].classList.add("active");
    currentSlideIndex = index;
  }

  // Function to move to next slide
  function nextSlide() {
    currentSlideIndex++;
    if (currentSlideIndex >= slides.length) {
      currentSlideIndex = 0;
    }
    showSlide(currentSlideIndex);
  }

  // Function to move to previous slide
  function prevSlide() {
    currentSlideIndex--;
    if (currentSlideIndex < 0) {
      currentSlideIndex = slides.length - 1;
    }
    showSlide(currentSlideIndex);
  }

  // Function to start auto-rotation
  function startAutoRotate() {
    // Clear any existing interval first
    if (slideInterval) {
      clearInterval(slideInterval);
    }

    // Only start if we have more than one slide
    if (slides.length > 1) {
      slideInterval = setInterval(nextSlide, autoRotateInterval);
    }
  }

  // Function to stop auto-rotation
  function stopAutoRotate() {
    if (slideInterval) {
      clearInterval(slideInterval);
    }
  }

  // Event listeners for prev/next buttons
  prevBtn.addEventListener("click", function (e) {
    e.preventDefault();
    prevSlide();
    // Reset the auto-rotation timer when manually navigating
    stopAutoRotate();
    startAutoRotate();
  });

  nextBtn.addEventListener("click", function (e) {
    e.preventDefault();
    nextSlide();
    // Reset the auto-rotation timer when manually navigating
    stopAutoRotate();
    startAutoRotate();
  });

  // Pause rotation when hovering over slideshow
  slideshowContainer.addEventListener("mouseenter", function () {
    stopAutoRotate();
  });

  // Resume rotation when mouse leaves slideshow
  slideshowContainer.addEventListener("mouseleave", function () {
    startAutoRotate();
  });

  // Initialize with first slide and start auto-rotation
  showSlide(0);
  startAutoRotate();
}


// for the cafe review form 
 // Get references to the button and the form container
 const toggleReviewFormBtn = document.getElementById("toggleReviewFormBtn");
 const reviewFormContainer = document.getElementById("reviewFormContainer");
 const starIcons = document.querySelectorAll("#starRating .star-icon");
 const selectedRatingInput = document.getElementById("selectedRating");

 let currentRating = 0; // Stores the permanently selected rating

 // Function to update star colors based on a given rating value
 function updateStarColors(ratingValue) {
     starIcons.forEach((star, index) => {
         if (index < ratingValue) {
             star.classList.remove("text-gray-300");
             star.classList.add("text-yellow-500"); // Yellow for selected stars
         } else {
             star.classList.remove("text-yellow-500");
             star.classList.add("text-gray-300"); // Gray for unselected stars
         }
     });
 }

 // Add event listeners to each star
 starIcons.forEach(star => {
     star.addEventListener("click", function() {
         // Set the current rating based on the clicked star's data-rating
         currentRating = parseInt(this.dataset.rating);
         // Update the hidden input value
         selectedRatingInput.value = currentRating;
         // Update star colors to reflect the permanent selection
         updateStarColors(currentRating);
     });

     star.addEventListener("mouseover", function() {
         // On hover, highlight stars up to the hovered one
         const hoverRating = parseInt(this.dataset.rating);
         updateStarColors(hoverRating);
     });

     star.addEventListener("mouseout", function() {
         // On mouse out, revert to the currently selected rating
         updateStarColors(currentRating);
     });
 });


 // Add event listener to the toggle button
 toggleReviewFormBtn.addEventListener("click", function () {
     // Toggle the 'hidden' Tailwind class to show/hide the form
     reviewFormContainer.classList.toggle("hidden");
     
     // Optional: You might want to change the button text based on form visibility
     if (reviewFormContainer.classList.contains("hidden")) {
         toggleReviewFormBtn.textContent = "Write a review about cafe";
     } else {
         toggleReviewFormBtn.textContent = "Hide review form";
     }
 });