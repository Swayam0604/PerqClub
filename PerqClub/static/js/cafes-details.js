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

// const cafeData = {
//   1: {
//     name: "Bombay To Barcelona Library Cafe",
//     location: "Andheri East, Mumbai",
//     mapUrl:
//       "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3769.9597775951183!2d72.88118109999999!3d19.109420399999998!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7c81359615555%3A0x477fa11ce01f0713!2sBombay%20To%20Barcelona%20Library%20Cafe!5e0!3m2!1sen!2sin!4v1744698275903!5m2!1sen!2sin",
//     rating: 4.6,
//     reviewCount: "2,635",
//     description:
//       "In August 2016, Amin Sheikh's dream came true with the inauguration of Bombay to Barcelona Library Café, a unique space run by girls and boys rescued from the streets of Mumbai who, thanks to Amin, have managed to change their lives and reintegrate into society.\n\nBombay to Barcelona brings a brand-new concept of cuisine by combining traditional Indian and European recipes that delight the most demanding palates. At the Café, we serve great food, honestly prepared, and simply served. A welcoming space where you will always be greeted with a big smile.",
//     images: [
//       "../static/img/cafe-1-img-1.jpg",
//       "../static/img/cafe-1-img-2.jpg",
//       "../static/img/cafe-1-img-3.webp",
//       "../static/img/cafe-1-img-4.jpg",
//       "../static/img/cafe-1-img-5.jpg",
//     ],
//     highlights: [
//       "Free WiFi",
//       "Power Outlets",
//       "Breakfast",
//       "Parking",
//       "Work-Friendly",
//       "Pet-Friendly",
//     ],
//     reviews: [
//       {
//         name: "Priya Sharma",
//         date: "2 days ago",
//         rating: 5,
//         text: "Absolutely love this place! The ambiance is perfect for working or casual catch-ups. Their cappuccino is to die for, and don't even get me started on their almond croissants. The staff is friendly, and with my membership card, I got a nice discount. Will definitely be back!",
//         helpfulCount: 15,
//       },
//       {
//         name: "Rohit Patel",
//         date: "1 week ago",
//         rating: 4,
//         text: "Great coffee but can get a bit crowded during peak hours. I used my membership card to get a free coffee and it was a smooth experience. The baristas really know their craft. Would recommend trying their pour-over - it's exceptional!",
//         helpfulCount: 7,
//       },
//       {
//         name: "Aishwarya Singh",
//         date: "2 week ago",
//         rating: 3.5,
//         text: "I love the vibe here! It's a perfect spot for meeting clients or getting some work done. The coffee is excellent, and they have good food options too. WiFi can be a bit spotty during busy hours, but overall a great café. The membership discount makes it even better value.",
//         helpfulCount: 7,
//       },
//       // Add more reviews
//     ],
//     nearbyCafes: [
//       {
//         id: 4,
//         distance: "0.5 km away",
//         shortDescription:
//           "A quiet space with books and great coffee. Perfect for the literary-minded.",
//       },
//       {
//         id: 12,
//         distance: "0.8 km away",
//         shortDescription:
//           "A comfortable cafe with quality drinks and snacks with a friendly atmosphere.",
//       },
//       {
//         id: 19,
//         distance: "1.2 km away",
//         shortDescription:
//           "Enjoy a wide selection of coffee, teas, and light bites.",
//       },
//     ],
//   },
//   2: {
//     name: "Kala Ghoda Cafe",
//     location: "Fort, Mumbai",
//     mapUrl:
//       "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3415.3326973011062!2d72.8322067!3d18.9284954!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7d1c30a9927b9%3A0x93f817f1a8e74b23!2sKala%20Ghoda%20Cafe!5e1!3m2!1sen!2sin!4v1744725102284!5m2!1sen!2sin", // Add actual map URL
//     rating: 4.3,
//     reviewCount: "5,043",
//     description:
//       "Kala Ghoda Cafe in Fort, Mumbai, is a popular spot known for its charming old-world vibe and modern take on the classic Mumbai cafe experience. It's a favorite for both locals and tourists seeking a relaxed atmosphere and a diverse menu. \n\nThe cafe boasts a cozy, comfortable, and slightly romantic atmosphere, with tall ceilings, AC, and ceiling fans. ",
//     images: [
//       "../static/img/cafe-2-img-1.jpg",
//       "../static/img/cafe-2-img-2.jpg",
//       "../static/img/cafe-2-img-3.jpg",
//       "../static/img/cafe-2-img-4.jpg",
//       "../static/img/cafe-2-img-5.jpg",
//     ],
//     highlights: [
//       "Free WiFi",
//       "Power Outlets",
//       "Pet-Friendly",
//       "Outdoor Seating",
//       "Work-Friendly",
//       "Air Conditioning",
//     ],
//     reviews: [
//       {
//         name: "Kunal Verma",
//         date: "3 days ago",
//         rating: 5,
//         text: "This is my go-to coffee shop! The atmosphere is so relaxing, and the staff always makes me feel welcome. Their latte art is impressive, and the pastries are always fresh. Highly recommend!",
//         helpfulCount: 12,
//       },
//       {
//         name: "Vikram Joshi",
//         date: "2 weeks ago",
//         rating: 5,
//         text: "Best cold brew I've had in the city! The flavor is rich and smooth. They also have a good selection of sandwiches for a quick lunch. The staff is always friendly and efficient.",
//         helpfulCount: 9,
//       },
//       {
//         name: "Divya Menon",
//         date: "4 days ago",
//         rating: 4,
//         text: "A nice and cozy place to grab a coffee and read a book. The music is chill, and the seating is comfortable. I tried their avocado toast, and it was delicious. Will definitely be back to try more from their menu.",
//         helpfulCount: 6,
//       },
//       // Add more reviews
//     ],
//     nearbyCafes: [
//       {
//         id: 13,
//         distance: "0.5 km away",
//         shortDescription:
//           "Freshly brewed coffee and a cozy spot to meet friends.",
//       },
//       {
//         id: 18,
//         distance: "0.8 km away",
//         shortDescription:
//           "Your everyday cafe for a reliable and enjoyable experience.",
//       },
//       {
//         id: 6,
//         distance: "1.2 km away",
//         shortDescription:
//           "Your go-to cafe for a morning boost or afternoon treat.",
//       },
//     ], // IDs of nearby cafes
//   },
//   3: {
//     name: "Poetry by Love & Cheesecake",
//     location: "Bandra West, Mumbai.",
//     mapUrl:
//       "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3412.5782148310764!2d72.8327868!3d19.0627843!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7c913a88861c1%3A0x77ae1c70f02af307!2sPoetry%20by%20Love%20and%20Cheesecake%2C%20Bandra%20W!5e1!3m2!1sen!2sin!4v1744728550656!5m2!1sen!2sin", // Add actual map URL
//     rating: 4.4,
//     reviewCount: 855,
//     description:
//       "Poetry by Love and Cheesecake is your go-to neighborhood cafe, serving American-European comfort food and classic beverages from dawn till dusk. With a playful sense of humor, affordable prices, and friendly service, you'll feel right at home as you indulge in our unique twists on everyday dishes. \n\nCome experience the warm hospitality of Ruchyeta and Chef Amit, a humble duo couple who have blended their entrepreneurship and culinary prowess to bring you a delightful dining experience.",
//     images: [
//       "../static/img/cafe-3-img-1.jpg",
//       "../static/img/cafe-3-img-2.jpg",
//       "../static/img/cafe-3-img-3.jpg",
//       "../static/img/cafe-3-img-4.jpg",
//       "../static/img/cafe-3-img-5.jpg",
//     ],
//     highlights: [
//       "Free WiFi",
//       "Power Outlets",
//       "Vegan Options",
//       "Outdoor Seating",
//       "Work-Friendly",
//       "Air Conditioning",
//     ],
//     reviews: [
//       {
//         name: "Siya Sharma",
//         date: "3 weeks ago",
//         rating: 5,
//         text: "Love the aesthetic of this café! It's very Instagram-worthy. More importantly, the coffee is fantastic, and they have a great selection of vegan options. The staff is also very knowledgeable about their products.",
//         helpfulCount: 11,
//       },
//       {
//         name: "Rohan Verma",
//         date: "5 days ago",
//         rating: 4,
//         text: "Good coffee and a pleasant atmosphere. It's a great place to work remotely. They have ample charging points and the WiFi is generally reliable. The prices are a bit on the higher side, though.",
//         helpfulCount: 8,
//       },
//       {
//         name: "Ananya Patel",
//         date: "1 week ago",
//         rating: 5,
//         text: "The service here is outstanding! The baristas are always so cheerful and helpful. Their seasonal drinks are always creative and delicious. I look forward to my daily coffee fix here.",
//         helpfulCount: 14,
//       },
//       // Add more reviews
//     ],
//     nearbyCafes: [
//       {
//         id: 5,
//         distance: "0.5 km away",
//         shortDescription:
//           "The ideal spot for your coffee break and a moment of calm.",
//       },
//       {
//         id: 8,
//         distance: "0.8 km away",
//         shortDescription:
//           "Stop by for a quick coffee break or stay and relax a while.",
//       },
//       {
//         id: 9,
//         distance: "1.2 km away",
//         shortDescription:
//           "Your daily dose of coffee and snacks with a welcoming smile.",
//       },
//     ], // IDs of nearby cafes
//   },
//   4: {
//     name: "Leaping Windows Café",
//     location: "Andheri West, Mumbai",
//     mapUrl:
//       "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3411.0109311368997!2d72.81339!3d19.1387888!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7b60fa977dd83%3A0x504f973f3b5d9668!2sLeaping%20Windows!5e1!3m2!1sen!2sin!4v1744730491897!5m2!1sen!2sin", // Add actual map URL
//     rating: 4.6,
//     reviewCount: "2,181",
//     description:
//       "Leaping Windows Cafe is a popular eatery located in Versova, Mumbai, known for its fast food and a cozy atmosphere with a good selection of books and comics.\n\nIt offers a variety of options on its menu, including starters like chicken wings, chicken skewers, and crispy fried chicken. They also serve pizzas and pastas, burgers and sandwiches, and desserts. The cafe is a good place to relax and enjoy a meal with a book, or to grab a quick bite.",
//     images: [
//       "../static/img/cafe-4-img-1.jpg",
//       "../static/img/cafe-4-img-2.jpg",
//       "../static/img/cafe-4-img-3.jpg",
//       "../static/img/cafe-4-img-4.jpg",
//       "../static/img/cafe-4-img-5.jpg",
//     ],
//     highlights: [
//       "Free WiFi",
//       "Power Outlets",
//       "Vegan Options",
//       "Outdoor Seating",
//       "Work-Friendly",
//       "Air Conditioning",
//     ],
//     reviews: [
//       {
//         name: "Meera Joshi",
//         date: "6 days ago",
//         rating: 5,
//         text: "Their matcha latte is the best I've ever had! So creamy and flavorful. The staff is always friendly and remembers my order. It feels like a little community hub.",
//         helpfulCount: 10,
//       },
//       {
//         name: "Varun Reddy",
//         date: "1 week ago",
//         rating: 4,
//         text: "A solid choice for coffee and a light bite. Their sandwiches are well-made, and they have a good variety of teas as well. The atmosphere is calm and conducive to work.",
//         helpfulCount: 7,
//       },
//       {
//         name: "Aryan Kapoor",
//         date: "7 days ago",
//         rating: 5,
//         text: "This café is a hidden gem! The coffee is consistently excellent, and the staff is incredibly welcoming. Their homemade cookies are a must-try!",
//         helpfulCount: 13,
//       },
//       // Add more reviews
//     ],
//     nearbyCafes: [
//       {
//         id: 12,
//         distance: "0.5 km away",
//         shortDescription:
//           "A comfortable cafe with quality drinks and snacks with a friendly atmosphere.",
//       },
//       {
//         id: 19,
//         distance: "0.8 km away",
//         shortDescription:
//           "Enjoy a wide selection of coffee, teas, and light bites.",
//       },
//       {
//         id: 20,
//         distance: "1.2 km away",
//         shortDescription:
//           "Your neighborhood spot for great coffee and a relaxed vibe.",
//       },
//     ], // IDs of nearby cafes
//   },
//   5: {
//     name: "Bombay Coffee House",
//     location: "Bandra West, Mumbai",
//     mapUrl:
//       "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3412.5690498152608!2d72.83475849999999!3d19.063229600000003!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7c916b18e64f7%3A0x411a7b22b06f266b!2sBombay%20Coffee%20House!5e1!3m2!1sen!2sin!4v1744730991835!5m2!1sen!2sin", // Add actual map URL
//     rating: 4.2,
//     reviewCount: "3,033",
//     description:
//       "Bombay Coffee House is an elegant coffee shop that serves a variety of Coffees, Savories, Hot Meals & Breakfast all day as well as a fully functioning patisserie. \n\nWe want to bring back the old days of going to a coffee shop for wholesome freshly made comfort food and conversations over a cup of coffee.",
//     images: [
//       "../static/img/cafe-5-img-1.jpg",
//       "../static/img/cafe-5-img-2.jpg",
//       "../static/img/cafe-5-img-3.jpg",
//       "../static/img/cafe-5-img-4.jpg",
//       "../static/img/cafe-5-img-5.jpg",
//     ],
//     highlights: [
//       "Free WiFi",
//       "Power Outlets",
//       "Vegan Options",
//       "Outdoor Seating",
//       "Work-Friendly",
//       "Air Conditioning",
//     ],
//     reviews: [
//       {
//         name: "Diya Sharma",
//         date: "2 weeks ago",
//         rating: 4,
//         text: "Enjoyed my visit here. The coffee was good, and the ambiance was pleasant. It's a bit noisy, but it has a lively feel. Their loyalty program is a nice perk.",
//         helpfulCount: 6,
//       },
//       {
//         name: "Pooja Patel",
//         date: "1 week ago",
//         rating: 5,
//         text: "Absolutely fantastic coffee and delicious pastries! The staff is always smiling and creates a warm atmosphere. It's my favorite place to start my day.",
//         helpfulCount: 16,
//       },
//       {
//         name: "Sameer Singh",
//         date: "3 weeks ago",
//         rating: 4,
//         text: "A great local café with a community feel. The coffee is consistently good, and they often have live music on weekends. It's a nice place to unwind.",
//         helpfulCount: 9,
//       },
//       // Add more reviews
//     ],
//     nearbyCafes: [
//       {
//         id: 3,
//         distance: "0.5 km away",
//         shortDescription:
//           "The perfect place to unwind with a good cup of coffee.",
//       },
//       {
//         id: 11,
//         distance: "0.8 km away",
//         shortDescription:
//           "Come experience our friendly service and delicious menu.",
//       },
//       {
//         id: 16,
//         distance: "1.2 km away",
//         shortDescription:
//           "A cozy and inviting Café & Bistro great option for a late-night meal or drink.",
//       },
//     ], // IDs of nearby cafes
//   },
//   6: {
//     name: "Mockingbird Café",
//     location: "Churchgate, Mumbai",
//     mapUrl:
//       "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d12443.683459701879!2d72.82007439062473!3d18.92806886495794!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7d1e7a1ae8dc5%3A0x470f3f1aff27975c!2sMockingbird%20Cafe%20Bar!5e1!3m2!1sen!2sin!4v1744731673350!5m2!1sen!2sin", // Add actual map URL
//     rating: 4.4,
//     reviewCount: "7,066",
//     description:
//       "Mockingbird café bar was conceived by Deepak Purohit. The idea was to marry the romance of reading and love of food and drinks together. We have created a space where one can relax; indulge one selves with a well curated food and bar menu and an eclectic collection of books with some great music adding to the laid back ambience. \n\nOur place is designed to stimulate your mind as well as your taste buds. To celebrate the art of conversation. A refuge far from the madding crowd. Bon appétit !!.",
//     images: [
//       "../static/img/cafe-6-img-1.jpg",
//       "../static/img/cafe-6-img-2.jpg",
//       "../static/img/cafe-6-img-3.jpg",
//       "../static/img/cafe-6-img-4.jpg",
//       "../static/img/cafe-6-img-5.jpg",
//     ],
//     highlights: [
//       "Free WiFi",
//       "Power Outlets",
//       "Vegan Options",
//       "Outdoor Seating",
//       "Work-Friendly",
//       "Air Conditioning",
//     ],
//     reviews: [
//       {
//         name: "Aisha Verma",
//         date: "5 days ago",
//         rating: 4.5,
//         text: "Loved the cozy vibes and great selection of coffee! The baristas are friendly, and the music adds to the relaxing atmosphere.",
//         helpfulCount: 8,
//       },
//       {
//         name: "Rohan Mehta",
//         date: "2 days ago",
//         rating: 5,
//         text: "Best café in town! Their cappuccino is perfect, and I appreciate their attention to detail. Always a pleasure to visit.",
//         helpfulCount: 14,
//       },
//       {
//         name: "Neha Joshi",
//         date: "1 week ago",
//         rating: 4,
//         text: "A great spot to catch up with friends. The coffee is rich and smooth, though weekends can be a bit crowded.",
//         helpfulCount: 10,
//       },
//       // Add more reviews
//     ],
//     nearbyCafes: [
//       {
//         id: 2,
//         distance: "0.5 km away",
//         shortDescription:
//           "Serving up delicious coffee and tasty treats all day long.",
//       },
//       {
//         id: 7,
//         distance: "0.8 km away",
//         shortDescription:
//           "Serving up delicious coffee and tasty treats all day long.",
//       },
//       {
//         id: 18,
//         distance: "1.2 km away",
//         shortDescription:
//           "Your everyday cafe for a reliable and enjoyable experience.",
//       },
//     ], // IDs of nearby cafes
//   },
//   7: {
//     name: "Brooke Bond Taj Mahal Tea House",
//     location: "Churchgate, Mumbai",
//     mapUrl:
//       "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2261.1565707756677!2d72.8225223997357!3d19.049073618226114!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7c94709994f15%3A0xbbc0becf5b6d3c1a!2sBrooke%20Bond%20Taj%20Mahal%20Tea%20House!5e1!3m2!1sen!2sin!4v1744732961863!5m2!1sen!2sin", // Add actual map URL
//     rating: 4.5,
//     reviewCount: "3,771",
//     description:
//       "Cocooned in a charming, old-worldly lane in Bandra, Mumbai, Brooke Bond Taj Mahal Tea House, appeals to tea connoisseurs, classical live music enthusiasts, book lovers, and many an artistic soul. Since its launch in 2015, the House has become synonymous with signature tea stories. \n\nIt features the choicest of fine Indian tea and tea blends curated by our tea sommeliers, constructed into authentic tea recipes.",
//     images: [
//       "../static/img/cafe-7-img-1.jpg",
//       "../static/img/cafe-7-img-2.jpg",
//       "../static/img/cafe-7-img-3.jpg",
//       "../static/img/cafe-7-img-4.jpg",
//       "../static/img/cafe-7-img-5.jpg",
//     ],
//     highlights: [
//       "Free WiFi",
//       "Power Outlets",
//       "Vegan Options",
//       "Outdoor Seating",
//       "Work-Friendly",
//       "Air Conditioning",
//     ],
//     reviews: [
//       {
//         name: "Kabir Gupta",
//         date: "3 weeks ago",
//         rating: 4.7,
//         text: "Their espresso shots are strong and satisfying. The seating is comfortable, and the service is quick.",
//         helpfulCount: 12,
//       },
//       {
//         name: "Aarav Nair",
//         date: "1 week ago",
//         rating: 5,
//         text: "Excellent staff, delicious pastries, and an overall welcoming environment! Their cold brew is a must-try.",
//         helpfulCount: 15,
//       },
//       {
//         name: "Sanya Rao",
//         date: "4 days ago",
//         rating: 4.3,
//         text: "The café is aesthetically pleasing, perfect for reading a book while sipping coffee. The flavors are bold and distinct.",
//         helpfulCount: 7,
//       },
//       // Add more reviews
//     ],
//     nearbyCafes: [
//       {
//         id: 2,
//         distance: "0.5 km away",
//         shortDescription:
//           "Serving up delicious coffee and tasty treats all day long.",
//       },
//       {
//         id: 6,
//         distance: "0.8 km away",
//         shortDescription:
//           "Your go-to cafe for a morning boost or afternoon treat.",
//       },
//       {
//         id: 18,
//         distance: "1.2 km away",
//         shortDescription:
//           "Your everyday cafe for a reliable and enjoyable experience.",
//       },
//     ], // IDs of nearby cafes
//   },
//   8: {
//     name: "Mary Lodge by Subko",
//     location: "Bandra West, Mumbai",
//     mapUrl:
//       "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d54614.56073572236!2d72.79129811865683!3d19.02232638157562!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7c9857a54fe43%3A0x24a2c7d62582f7ff!2sMary%20Lodge%20by%20Subko!5e1!3m2!1sen!2sin!4v1744737673224!5m2!1sen!2sin", // Add actual map URL
//     rating: 4.3,
//     reviewCount: "2,587",
//     description:
//       "Subko at Mary Lodge is more than just a cafe; it's a destination for coffee aficionados and food lovers alike. Indulge in their innovative coffee creations, from classic espresso to unique blends and manual brews. Pair your perfect cup with their delectable selection of pastries, including flaky croissants and flavorful sourdough, alongside other tempting baked delights. Beyond the coffee and pastries, you'll find a curated menu of sandwiches, bowls, and desserts, often featuring creative flavor combinations.",
//     images: [
//       "../static/img/cafe-8-img-1.jpg",
//       "../static/img/cafe-8-img-2.jpg",
//       "../static/img/cafe-8-img-3.jpg",
//       "../static/img/cafe-8-img-4.jpg",
//       "../static/img/cafe-8-img-5.jpg",
//     ],
//     highlights: [
//       "Free WiFi",
//       "Power Outlets",
//       "Vegan Options",
//       "Outdoor Seating",
//       "Work-Friendly",
//       "Air Conditioning",
//     ],
//     reviews: [
//       {
//         name: "Varun Malhotra",
//         date: "2 weeks ago",
//         rating: 4.8,
//         text: "I love their oat milk latte! The place has a charming appeal, and the loyalty program makes it even better.",
//         helpfulCount: 11,
//       },
//       {
//         name: "Meera Desai",
//         date: "1 week ago",
//         rating: 4.5,
//         text: "Consistently good coffee and friendly service. The ambiance is warm, making it an ideal spot for casual meetings.",
//         helpfulCount: 9,
//       },
//       {
//         name: "Vikram Khanna",
//         date: "3 weeks ago",
//         rating: 5,
//         text: "The pastries here are to die for! The coffee is top-notch, and their attention to customer satisfaction is evident.",
//         helpfulCount: 13,
//       },
//       // Add more reviews
//     ],
//     nearbyCafes: [
//       {
//         id: 3,
//         distance: "0.5 km away",
//         shortDescription:
//           "The perfect place to unwind with a good cup of coffee.",
//       },
//       {
//         id: 5,
//         distance: "0.8 km away",
//         shortDescription:
//           "The ideal spot for your coffee break and a moment of calm.",
//       },
//       {
//         id: 9,
//         distance: "1.2 km away",
//         shortDescription:
//           "Your daily dose of coffee and snacks with a welcoming smile.",
//       },
//     ], // IDs of nearby cafes
//   },
//   9: {
//     name: "Candies",
//     location: "Bandra West, Mumbai",
//     mapUrl:
//       "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d54601.81047094784!2d72.75665285820311!3d19.061086600000007!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7c96b3b51538b%3A0xaddb4eebfe34c0fe!2sCandies!5e1!3m2!1sen!2sin!4v1744739514138!5m2!1sen!2sin", // Add actual map URL
//     rating: 4.3,
//     reviewCount: "17,170",
//     description:
//       "Just these three words are enough to summarize everything that Candies stands for! In the business for the last 25 years, Candies has come a long way from a humble kitchen to 3 full-fledged operational branches in Bandra.The menu boasts of a mixed cuisine including a variety of snacks, main courses, desserts and drinks. With a wide selection of sandwiches, rolls, salads, mini meals and scrumptious sweet treats to choose from there's something for everyone. Whether you are looking for food for the soul a quick bite on your way to work or a place to indulge in conversation over coffee, this is the place to be.",
//     images: [
//       "../static/img/cafe-9-img-1.jpg",
//       "../static/img/cafe-9-img-2.jpg",
//       "../static/img/cafe-9-img-3,jpg.webp",
//       "../static/img/cafe-9-img-4.jpg",
//       "../static/img/cafe-9-img-5.jpg",
//     ],
//     highlights: [
//       "Free WiFi",
//       "Power Outlets",
//       "Vegan Options",
//       "Outdoor Seating",
//       "Work-Friendly",
//       "Air Conditioning",
//     ],
//     reviews: [
//       {
//         name: "Priya Shah",
//         date: "6 days ago",
//         rating: 4.2,
//         text: "A great neighborhood café with a relaxing vibe. The iced mocha was perfect, and the staff made me feel welcome.",
//         helpfulCount: 6,
//       },
//       {
//         name: "Rahul Saxena",
//         date: "2 weeks ago",
//         rating: 4.6,
//         text: "A hidden gem! Their freshly ground coffee beans enhance the taste. Will definitely be coming back.",
//         helpfulCount: 12,
//       },
//       {
//         name: "Shweta Iyer",
//         date: "1 week ago",
//         rating: 4.4,
//         text: "The café has a vibrant energy and serves really good coffee. I wish they had more outdoor seating, though.",
//         helpfulCount: 8,
//       },
//       // Add more reviews
//     ],
//     nearbyCafes: [
//       {
//         id: 11,
//         distance: "0.5 km away",
//         shortDescription:
//           "Come experience our friendly service and delicious menu.",
//       },
//       {
//         id: 16,
//         distance: "0.8 km away",
//         shortDescription:
//           "A cozy and inviting Café & Bistro great option for a late-night meal or drink.",
//       },
//       {
//         id: 3,
//         distance: "1.2 km away",
//         shortDescription:
//           "Your daily dose of coffee and snacks with a welcoming smile.",
//       },
//     ], // IDs of nearby cafes
//   },
//   10: {
//     name: "Prithvi Cafe",
//     location: "Juhu, Mumbai",
//     mapUrl:
//       "https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d11476.09910114!2d72.8278036610402!3d19.097423059111726!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7c9ea57688fa3%3A0xefc0e4027133d0bc!2sPrithvi%20Cafe!5e1!3m2!1sen!2sin!4v1744797763820!5m2!1sen!2sin", // Add actual map URL
//     rating: 4.4,
//     reviewCount: "18,512",
//     description:
//       "Prithvi Cafe is a popular cafe located within the Prithvi Theatre compound in Mumbai, known for its garden ambiance, a wide variety of food and drinks, and its connection to the theatre. It's a favorite spot for locals and tourists, especially those interested in the performing arts. \n\neatures an open-air garden setting with lanterns, trees, and bamboo.",
//     images: [
//       "../static/img/cafe-10-img-1.jpg",
//       "../static/img/cafe-10-img-2.jpg",
//       "../static/img/cafe-10-img-3.jpg",
//       "../static/img/cafe-10-img-4.jpg",
//       "../static/img/cafe-10-img-5.jpg",
//     ],
//     highlights: [
//       "Free WiFi",
//       "Power Outlets",
//       "Vegan Options",
//       "Outdoor Seating",
//       "Work-Friendly",
//       "Air Conditioning",
//     ],
//     reviews: [
//       {
//         name: "Anirudh Pillai",
//         date: "3 weeks ago",
//         rating: 4.9,
//         text: "An amazing café experience! Their chai latte was surprisingly delicious, and the service was impeccable.",
//         helpfulCount: 14,
//       },
//       {
//         name: "Ishita Das",
//         date: "6 days ago",
//         rating: 4,
//         text: "Perfect place for an afternoon coffee break. The desserts complement the beverages really well.",
//         helpfulCount: 7,
//       },
//       {
//         name: "Kunal Aggarwal",
//         date: "2 weeks ago",
//         rating: 4.7,
//         text: "A must-visit for coffee lovers! The atmosphere is warm, and their baristas really know their craft.",
//         helpfulCount: 11,
//       },
//       // Add more reviews
//     ],
//     nearbyCafes: [
//       {
//         id: 12,
//         distance: "0.5 km away",
//         shortDescription:
//           "A comfortable cafe with quality drinks and snacks with a friendly atmosphere.",
//       },
//       {
//         id: 14,
//         distance: "0.8 km away",
//         shortDescription:
//           "Enjoy expertly brewed coffee in a friendly atmosphere.",
//       },
//       {
//         id: 17,
//         distance: "1.2 km away",
//         shortDescription:
//           "Serving up your favorite coffee and creating community.",
//       },
//     ], // IDs of nearby cafes
//   },
//   11: {
//     name: "The Bandstand Pantry",
//     location: "Bandra West, Mumbai",
//     mapUrl:
//       "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3412.892604526634!2d72.8201545!3d19.047503!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7c9f4debe96c3%3A0x74823fe89214dab2!2sThe%20Bandstand%20Pantry!5e1!3m2!1sen!2sin!4v1744799509002!5m2!1sen!2sin", // Add actual map URL
//     rating: 4.2,
//     reviewCount: 602,
//     description:
//       "The Bandstand Pantry's menu can best be described as grown-up breakfast food. Think scrambled or folded omelette filled with oven-roasted Portobello mushrooms, slow-cooked and house-made veal pastrami and truffle smoked salmon. The soft-poached eggs are served on English muffins topped with a Hass avo and Kashmiri walnut and the Greek yoghurt bowl is a delightful mainstay.If you are here in the PM, you don't have to commit to brekkie food—they have other options too. Like a country sourdough toast topped with pesto marinated bocconcini, chunky peanut butter, fruit marmalade and cream cheese sandwiches, and slow-roasted chicken, macaroni and Jack cheese skillet.",
//     images: [
//       "../static/img/cafe-11-img-1.jpg",
//       "../static/img/cafe-11-img-2.jpg",
//       "../static/img/cafe-11-img-3.jpg",
//       "../static/img/cafe-11-img-4.jpg",
//       "../static/img/cafe-11-img-5.jpg",
//     ],
//     highlights: [
//       "Free WiFi",
//       "Power Outlets",
//       "Vegan Options",
//       "Outdoor Seating",
//       "Work-Friendly",
//       "Air Conditioning",
//     ],
//     reviews: [
//       {
//         name: "Simran Kaur",
//         date: "1 week ago",
//         rating: 4.5,
//         text: "Love the artsy décor and cozy seats. The coffee quality never disappoints, and they have great vegan options too.",
//         helpfulCount: 10,
//       },
//       {
//         name: "Dev Sharma",
//         date: "3 weeks ago",
//         rating: 5,
//         text: "Their flat white is beautifully crafted. It's a great place to sit, work, and enjoy quality coffee.",
//         helpfulCount: 15,
//       },
//       {
//         name: "Pallavi Reddy",
//         date: "4 days ago",
//         rating: 4.3,
//         text: "A peaceful corner in a bustling city. The coffee is fragrant, and the staff is attentive.",
//         helpfulCount: 9,
//       },
//       // Add more reviews
//     ],
//     nearbyCafes: [
//       {
//         id: 5,
//         distance: "0.5 km away",
//         shortDescription:
//           "The ideal spot for your coffee break and a moment of calm.",
//       },
//       {
//         id: 8,
//         distance: "0.8 km away",
//         shortDescription:
//           "Stop by for a quick coffee break or stay and relax a while.",
//       },
//       {
//         id: 9,
//         distance: "1.2 km away",
//         shortDescription:
//           "Your daily dose of coffee and snacks with a welcoming smile.",
//       },
//     ], // IDs of nearby cafes
//   },
//   12: {
//     name: "Coffee by Di Bella",
//     location: "Versova, Andheri West, Mumbai",
//     mapUrl:
//       "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d109155.93053711238!2d72.67146121640623!3d19.133372000000005!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7c9e1f8fc2a53%3A0x75d9943f2dc5fdb3!2sCoffee%20By%20Di%20Bella%20Versova!5e1!3m2!1sen!2sin!4v1744801777031!5m2!1sen!2sin", // Add actual map URL
//     rating: 4.1,
//     reviewCount: "2,886",
//     description:
//       'Coffee By Di Bella Versova in Versova, Mumbai, is a popular coffee shop and cafe known for its coffee, shakes, waffles, and desserts. They are also known for their Australian-style coffee and "freakshakes". The cafe is a popular spot for locals and those from other parts of Mumbai, with a wide range of options catering to various tastes. ',
//     images: [
//       "../static/img/cafe-12-img-1.jpg",
//       "../static/img/cafe-12-img-2.jpg",
//       "../static/img/cafe-12-img-3.jpg",
//       "../static/img/cafe-12-img-4.jpg",
//       "../static/img/cafe-12-img-5.jpg",
//     ],
//     highlights: [
//       "Free WiFi",
//       "Power Outlets",
//       "Vegan Options",
//       "Outdoor Seating",
//       "Work-Friendly",
//       "Air Conditioning",
//     ],
//     reviews: [
//       {
//         name: "Harsh Trivedi",
//         date: "1 week ago",
//         rating: 4.6,
//         text: "Friendly service, amazing coffee, and a relaxed setting! What more could one ask for?",
//         helpfulCount: 13,
//       },
//       {
//         name: "Sneha Chatterjee",
//         date: "2 weeks ago",
//         rating: 4.5,
//         text: "Warm, inviting, and an overall delightful café. The ambiance makes every visit enjoyable.",
//         helpfulCount: 11,
//       },
//       {
//         name: "Tanvi Kapoor",
//         date: "3 days ago",
//         rating: 4.5,
//         text: "A lovely café with warm lighting and friendly staff. The hazelnut latte was delightful!",
//         helpfulCount: 7,
//       },
//       // Add more reviews
//     ],
//     nearbyCafes: [
//       {
//         id: 15,
//         distance: "0.5 km away",
//         shortDescription:
//           "Your local cafe for best quality filtered coffee and south indian breakfast a friendly face.",
//       },
//       {
//         id: 19,
//         distance: "0.8 km away",
//         shortDescription:
//           "Enjoy a wide selection of coffee, teas, and light bites.",
//       },
//       {
//         id: 20,
//         distance: "1.2 km away",
//         shortDescription:
//           "Your neighborhood spot for great coffee and a relaxed vibe.",
//       },
//     ], // IDs of nearby cafes
//   },
//   13: {
//     name: "The Nutcracker",
//     location: "Fort, Mumbai",
//     mapUrl:
//       "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3415.335230029735!2d72.8337416!3d18.9283715!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7d1c3808a06e7%3A0x8d5a681939c46f10!2sThe%20Nutcracker!5e1!3m2!1sen!2sin!4v1744806530244!5m2!1sen!2sin", // Add actual map URL
//     rating: 4.4,
//     reviewCount: "3,041",
//     description:
//       "The Nutcracker was founded in 2014 with its flagship cafe in Kala Ghoda, a precious corner of Mumbai known for its rich heritage and to be its art precinct. While it was a small beginning, it brought to life a big dream for us. Working patiently towards its creation we watched with excitement our vision translate into actual brick and mortar.... this was the start of our food journey!!. \n\nOur menu put vegetarianism into the limelight, drawing from ingredients and flavours that were local and global and always focusing on freshness and high quality ingredients. ",
//     images: [
//       "../static/img/cafe-13-img-1.jpg",
//       "../static/img/cafe-13-img-2.jpg",
//       "../static/img/cafe-13-img-3.jpg",
//       "../static/img/cafe-13-img-4.jpg",
//       "../static/img/cafe-13-img-5.jpg",
//     ],
//     highlights: [
//       "Free WiFi",
//       "Power Outlets",
//       "Vegan Options",
//       "Outdoor Seating",
//       "Work-Friendly",
//       "Air Conditioning",
//     ],
//     reviews: [
//       {
//         name: "Karan Menon",
//         date: "1 week ago",
//         rating: 5,
//         text: "Outstanding espresso shots and a great variety of pastries. The place is inviting and cozy.",
//         helpfulCount: 13,
//       },
//       {
//         name: "Aditi Bansal",
//         date: "2 weeks ago",
//         rating: 4.2,
//         text: "A great little hideaway with quality coffee. Wish they had more seating, but overall a great experience.",
//         helpfulCount: 9,
//       },
//       {
//         name: "Arjun Sethi",
//         date: "4 days ago",
//         rating: 4.7,
//         text: "Loved their caramel macchiato! The music selection is great, and the service is top-notch.",
//         helpfulCount: 12,
//       },

//       // Add more reviews
//     ],
//     nearbyCafes: [
//       {
//         id: 18,
//         distance: "0.5 km away",
//         shortDescription:
//           "Your everyday cafe for a reliable and enjoyable experience.",
//       },
//       {
//         id: 2,
//         distance: "0.8 km away",
//         shortDescription:
//           "Serving up delicious coffee and tasty treats all day long.",
//       },
//       {
//         id: 6,
//         distance: "1.2 km away",
//         shortDescription:
//           "Your go-to cafe for a morning boost or afternoon treat.",
//       },
//     ], // IDs of nearby cafes
//   },
//   14: {
//     name: "Grandmama's Cafe ",
//     location: "Juhu, Mumbai",
//     mapUrl:
//       "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d213.24930193675146!2d72.82793378527883!3d19.091400295965023!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7c9dffe4adb79%3A0xb2804cd270b6e562!2sGrandmama&#39;s%20Cafe%20Juhu!5e1!3m2!1sen!2sin!4v1744811744772!5m2!1sen!2sin", // Add actual map URL
//     rating: 4.0,
//     reviewCount: 511,
//     description:
//       "In a day and age where the importance of restaurant decor has dwindled down to stark furnishings and minimal personal touches, Grandmama's Café shines through with its most unique spin on a café. It can be whatever you want it to be – your favourite cozy corner at home, your grandmother's old house filled with memories or even your very own personal tea party in Wonderland!",
//     images: [
//       "../static/img/cafe-14-img-1.jpg",
//       "../static/img/cafe-14-img-2.jpg",
//       "../static/img/cafe-14-img-3.jpg",
//       "../static/img/cafe-14-img-4.jpg",
//       "../static/img/cafe-14-img-5.jpg",
//     ],
//     highlights: [
//       "Free WiFi",
//       "Power Outlets",
//       "Vegan Options",
//       "Outdoor Seating",
//       "Work-Friendly",
//       "Air Conditioning",
//     ],
//     reviews: [
//       {
//         name: "Madhuri Rao",
//         date: "1 week ago",
//         rating: 4.4,
//         text: "The café is well-maintained with fresh ingredients. Their cinnamon rolls are incredible!",
//         helpfulCount: 10,
//       },
//       {
//         name: "Sahil Chawla",
//         date: "2 weeks ago",
//         rating: 5,
//         text: "One of the best cafés in town! Their mocha was perfect, and the atmosphere is great.",
//         helpfulCount: 15,
//       },
//       {
//         name: "Ananya Sen",
//         date: "6 days ago",
//         rating: 4.3,
//         text: "A nice spot to work with strong Wi-Fi and delicious coffee. It does get busy, though!",
//         helpfulCount: 8,
//       },
//       // Add more reviews
//     ],
//     nearbyCafes: [
//       {
//         id: 10,
//         distance: "0.5 km away",
//         shortDescription:
//           "We're passionate about coffee and creating a welcoming space.",
//       },
//       {
//         id: 12,
//         distance: "0.8 km away",
//         shortDescription:
//           "A comfortable cafe with quality drinks and snacks with a friendly atmosphere.",
//       },
//       {
//         id: 17,
//         distance: "1.2 km away",
//         shortDescription:
//           "Serving up your favorite coffee and creating community.",
//       },
//     ], // IDs of nearby cafes
//   },
//   15: {
//     name: "Cafe Madras",
//     location: "Matunga East, Mumbai",
//     mapUrl:
//       "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d109225.64152487704!2d72.71496581640622!3d19.02762030000001!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7cf28fa60319d%3A0xf8101e76f66ded35!2zQ2FmZSBNYWRyYXPCru-4jw!5e1!3m2!1sen!2sin!4v1744812171236!5m2!1sen!2sin", // Add actual map URL
//     rating: 4.4,
//     reviewCount: "24,747",
//     description:
//       "Cafe Madras is a popular South Indian restaurant in Matunga East, Mumbai, known for its traditional dishes and lively atmosphere. They offer a variety of breakfast, lunch, and dinner options, including vegetarian and non-vegetarian dishes. Some popular dishes include masala dosa, idli sambar, and filter coffee. The restaurant has a casual and unpretentious vibe, making it a great place to enjoy a quick and tasty meal, and can accommodate larger groups.",
//     images: [
//       "../static/img/cafe-15-img-1.jpg",
//       "../static/img/cafe-15-img-2.jpg",
//       "../static/img/cafe-15-img-3.jpg",
//       "../static/img/cafe-15-img-4.jpg",
//       "../static/img/cafe-15-img-5.jpg",
//     ],
//     highlights: [
//       "Free WiFi",
//       "Power Outlets",
//       "Vegan Options",
//       "Outdoor Seating",
//       "Work-Friendly",
//       "Air Conditioning",
//     ],
//     reviews: [
//       {
//         name: "Rajesh Iyer",
//         date: "3 weeks ago",
//         rating: 4.8,
//         text: "Exceptional service and consistently great coffee! Their almond croissants are amazing.",
//         helpfulCount: 14,
//       },
//       {
//         name: "Pooja Rawat",
//         date: "2 days ago",
//         rating: 4.6,
//         text: "Enjoyed my visit! The cappuccino was smooth, and the ambiance is calming.",
//         helpfulCount: 11,
//       },
//       {
//         name: "Neil Dutta",
//         date: "1 week ago",
//         rating: 4.5,
//         text: "Superb coffee selection and a friendly team. Their loyalty program makes it worth coming back.",
//         helpfulCount: 9,
//       },
//       // Add more reviews
//     ],
//     nearbyCafes: [
//       {
//         id: 18,
//         distance: "0.5 km away",
//         shortDescription:
//           "Your everyday cafe for a reliable and enjoyable experience.",
//       },
//       {
//         id: 2,
//         distance: "0.8 km away",
//         shortDescription:
//           "Serving up delicious coffee and tasty treats all day long.",
//       },
//       {
//         id: 13,
//         distance: "1.2 km away",
//         shortDescription:
//           "Freshly brewed coffee and a cozy spot to meet friends.",
//       },
//     ], // IDs of nearby cafes
//   },
//   16: {
//     name: "Aromas Café & Bistro",
//     location: "Bandra West, Mumbai",
//     mapUrl:
//       "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d149673.65227422325!2d72.70283295381238!3d19.08409858240626!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7c938451909b7%3A0x32553165c90f9920!2sAromas%20Caf%C3%A9%20%26%20Bistro!5e1!3m2!1sen!2sin!4v1744814934248!5m2!1sen!2sin", // Add actual map URL
//     rating: 4.3,
//     reviewCount: 1568,
//     description:
//       "Aromas Café & Bistro is a popular spot in Bandra West, known for its elegant interior, cozy atmosphere, and delicious food. It's open late, making it a great option for a late-night meal or drink. They offer a wide variety of dishes, including breakfast, brunch, lunch, and dinner options. They also have a good selection of drinks, including coffee, wine, and beer.",
//     images: [
//       "../static/img/cafe-16-img-1.jpg",
//       "../static/img/cafe-16-img-2.jpg",
//       "../static/img/cafe-16-img-3.jpg",
//       "../static/img/cafe-16-img-4.jpg",
//       "../static/img/cafe-16-img-5.jpg",
//     ],
//     highlights: [
//       "Free WiFi",
//       "Power Outlets",
//       "Vegan Options",
//       "Outdoor Seating",
//       "Work-Friendly",
//       "Air Conditioning",
//     ],
//     reviews: [
//       {
//         name: "Ritika Gupta",
//         date: "5 days ago",
//         rating: 4.9,
//         text: "Great place for a quick coffee break. Their dark roast has incredible depth.",
//         helpfulCount: 13,
//       },
//       {
//         name: "Vishal Tandon",
//         date: "2 weeks ago",
//         rating: 4.2,
//         text: "A calm little café with friendly staff. The vanilla latte was enjoyable.",
//         helpfulCount: 7,
//       },
//       {
//         name: "Esha Mishra",
//         date: "3 days ago",
//         rating: 4.7,
//         text: "Loved the bright and airy setting. The iced coffee is super refreshing!",
//         helpfulCount: 12,
//       },
//       // Add more reviews
//     ],
//     nearbyCafes: [
//       {
//         id: 11,
//         distance: "0.5 km away",
//         shortDescription:
//           "Come experience our friendly service and delicious menu.",
//       },
//       {
//         id: 3,
//         distance: "0.8 km away",
//         shortDescription:
//           "The perfect place to unwind with a good cup of coffee.",
//       },
//       {
//         id: 5,
//         distance: "1.2 km away",
//         shortDescription:
//           "The ideal spot for your coffee break and a moment of calm.",
//       },
//     ], // IDs of nearby cafes
//   },
//   17: {
//     name: "Garde Manger Café",
//     location: "Vile Parle East, Mumbai",
//     mapUrl:
//       "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3411.712399294063!2d72.8522921!3d19.1048075!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7c84ab064da91%3A0xf60db7187c30646d!2sGarde%20Manger%20Cafe!5e1!3m2!1sen!2sin!4v1744816536711!5m2!1sen!2sin", // Add actual map URL
//     rating: 4.3,
//     reviewCount: "1,718",
//     description:
//       "Garde Manger Cafe offers a variety of food and drinks. They likely serve breakfast items, though this is not explicitly stated. For lunch and dinner, they offer salads, sandwiches, wraps, pasta dishes, and grilled items. They also have coffee, desserts, and a variety of vegetarian and vegan options. Additionally, Garde Manger Cafe has a full bar, so they likely offer alcoholic beverages.Sources and related content",
//     images: [
//       "../static/img/cafe-17-img-1.jpg",
//       "../static/img/cafe-17-img-2.jpg",
//       "../static/img/cafe-17-img-3.jpg",
//       "../static/img/cafe-17-img-4.jpg",
//       "../static/img/cafe-17-img-5.jpg",
//     ],
//     highlights: [
//       "Free WiFi",
//       "Power Outlets",
//       "Vegan Options",
//       "Outdoor Seating",
//       "Work-Friendly",
//       "Air Conditioning",
//     ],
//     reviews: [
//       {
//         name: "Aditya Malhotra",
//         date: "1 week ago",
//         rating: 4.6,
//         text: "Freshly brewed coffee with amazing texture. The food options are great too!",
//         helpfulCount: 11,
//       },
//       {
//         name: "Shruti Jindal",
//         date: "2 weeks ago",
//         rating: 4.4,
//         text: "A wonderful neighborhood café with aromatic coffee. Their muffins are a must-try!",
//         helpfulCount: 10,
//       },
//       {
//         name: "Kabir Das",
//         date: "4 days ago",
//         rating: 5,
//         text: "Amazing coffee, great ambiance, and friendly staff! The best morning stop.",
//         helpfulCount: 15,
//       },
//       // Add more reviews
//     ],
//     nearbyCafes: [
//       {
//         id: 4,
//         distance: "0.5 km away",
//         shortDescription:
//           "A quiet space with books and great coffee. Perfect for the literary-minded.",
//       },
//       {
//         id: 12,
//         distance: "0.8 km away",
//         shortDescription:
//           "A comfortable cafe with quality drinks and snacks with a friendly atmosphere.",
//       },
//       {
//         id: 19,
//         distance: "1.2 km away",
//         shortDescription:
//           "Enjoy a wide selection of coffee, teas, and light bites.",
//       },
//     ], // IDs of nearby cafes
//   },
//   18: {
//     name: "Café New York",
//     location: "Chowpatty, Mumbai",
//     mapUrl:
//       "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3414.7292141569114!2d72.8109848!3d18.9579953!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7ce0ea7ef5ff5%3A0xb74b40bfdf20ec11!2sCaf%C3%A9%20New%20York!5e1!3m2!1sen!2sin!4v1744817665127!5m2!1sen!2sin", // Add actual map URL
//     rating: 4.2,
//     reviewCount: "3,252",
//     description:
//       "Café New York is a long-standing restaurant and bar with a casual vibe, offering an American, Indian, and Chinese menu. It's open 24/7, making it a convenient spot any time of day. The cafe has a retro vibe and a diverse menu featuring tasty snacks, local, and international dishes. The atmosphere is casual and cozy, ideal for a relaxed meal with friends or a quick bite.",
//     images: [
//       "../static/img/cafe-18-img-1.jpg",
//       "../static/img/cafe-18-img-2.jpg",
//       "../static/img/cafe-18-img-3.jpg",
//       "../static/img/cafe-18-img-4.jpg",
//       "../static/img/cafe-18-img-5.jpg",
//     ],
//     highlights: [
//       "Free WiFi",
//       "Power Outlets",
//       "Vegan Options",
//       "Outdoor Seating",
//       "Work-Friendly",
//       "Air Conditioning",
//     ],
//     reviews: [
//       {
//         name: "Dia Mehta",
//         date: "1 week ago",
//         rating: 4.3,
//         text: "This café has a relaxed vibe and wonderful coffee! Perfect for unwinding.",
//         helpfulCount: 8,
//       },
//       {
//         name: "Rohan Kapoor",
//         date: "2 weeks ago",
//         rating: 4.5,
//         text: "Great café with quality coffee and delicious cookies! Will be coming back.",
//         helpfulCount: 9,
//       },
//       {
//         name: "Sanya Bhatt",
//         date: "6 days ago",
//         rating: 4.8,
//         text: "Fantastic latte and a peaceful atmosphere. This café is a real gem!",
//         helpfulCount: 14,
//       },
//       // Add more reviews
//     ],
//     nearbyCafes: [
//       {
//         id: 2,
//         distance: "0.5 km away",
//         shortDescription:
//           "Serving up delicious coffee and tasty treats all day long.",
//       },
//       {
//         id: 7,
//         distance: "0.8 km away",
//         shortDescription:
//           "Serving up delicious coffee and tasty treats all day long.",
//       },
//       {
//         id: 18,
//         distance: "1.2 km away",
//         shortDescription:
//           "Your everyday cafe for a reliable and enjoyable experience.",
//       },
//     ], // IDs of nearby cafes
//   },
//   19: {
//     name: "August Cafe",
//     location: " Andheri West, Mumbai",
//     mapUrl:
//       "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3411.039561356575!2d72.82703939999999!3d19.137403!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7b6181c9ac959%3A0xbd0f2243403e1bdc!2sAugust%20Cafe!5e1!3m2!1sen!2sin!4v1744819007993!5m2!1sen!2sin", // Add actual map URL
//     rating: 4.3,
//     reviewCount: "2,164",
//     description:
//       "August Cafe is a popular 24/7 cafe in Andheri West, known for its delicious Italian, Continental, Pan-Asian, and Mediterranean cuisine. It features a casual and cozy atmosphere, offering a wide range of dishes from breakfast to dinner, including healthy options and desserts. 1  Enjoy popular items like their caramel panacotta and Belgian hot chocolate. 2  August Cafe provides amenities such as outdoor seating, is wheelchair accessible, and offers parking. They accept various payment methods, including cards and NFC. It's a great spot for groups and children, offering options for dine-in, takeout, and delivery.",
//     images: [
//       "../static/img/cafe-19-img-1.jpg",
//       "../static/img/cafe-19-img-2.jpg",
//       "../static/img/cafe-19-img-3.jpg",
//       "../static/img/cafe-19-img-4.jpg",
//       "../static/img/cafe-19-img-5.jpg",
//     ],
//     highlights: [
//       "Free WiFi",
//       "Power Outlets",
//       "Vegan Options",
//       "Outdoor Seating",
//       "Work-Friendly",
//       "Air Conditioning",
//     ],
//     reviews: [
//       {
//         name: "Ishaan Tripathi",
//         date: "5 days ago",
//         rating: 4.7,
//         text: "Absolutely love this café! Their matcha latte is perfectly balanced, and the staff is incredibly welcoming.",
//         helpfulCount: 10,
//       },
//       {
//         name: "Mira Kulkarni",
//         date: "2 weeks ago",
//         rating: 4.3,
//         text: "A wonderful place to sit and relax with a book. Their freshly brewed coffee is delightful!",
//         helpfulCount: 7,
//       },
//       {
//         name: "Jayant Rao",
//         date: "1 week ago",
//         rating: 4.6,
//         text: "The espresso was smooth and rich in flavor. Definitely one of the best cafés in the area.",
//         helpfulCount: 12,
//       },
//       // Add more reviews
//     ],
//     nearbyCafes: [
//       {
//         id: 12,
//         distance: "0.5 km away",
//         shortDescription:
//           "A comfortable cafe with quality drinks and snacks with a friendly atmosphere.",
//       },
//       {
//         id: 19,
//         distance: "0.8 km away",
//         shortDescription:
//           "Enjoy a wide selection of coffee, teas, and light bites.",
//       },
//       {
//         id: 20,
//         distance: "1.2 km away",
//         shortDescription:
//           "Your neighborhood spot for great coffee and a relaxed vibe.",
//       },
//     ], // IDs of nearby cafes
//   },
//   20: {
//     name: "The C Spot Cafe",
//     location: "Andheri West, Mumbai",
//     mapUrl:
//       "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3410.7590943161863!2d72.8356675!3d19.1509744!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7b7daa0fcaca3%3A0x6ee4385037d56d96!2sThe%20C%20Spot%20Cafe!5e1!3m2!1sen!2sin!4v1744906528678!5m2!1sen!2sin", // Add actual map URL
//     rating: 4.7,
//     reviewCount: 156,
//     description:
//       "Coffee Culture is a premium cafe offering specialty coffees in a modern, welcoming setting. Known for their artisanal brewing methods and fresh pastries, this cafe has become a favorite among locals and tourists alike.\n\nTheir skilled baristas create perfect cups every time, using ethically sourced beans from around the world. The cozy atmosphere makes it an ideal spot for both work meetings and casual catch-ups.",
//     images: [
//       "../static/img/cafe-20-img-1.jpg",
//       "../static/img/cafe-20-img-2.jpg",
//       "../static/img/cafe-20-img-3.jpg",
//       "../static/img/cafe-20-img-4.jpg",
//       "../static/img/cafe-20-img-5.jpg",
//     ],
//     highlights: [
//       "Free WiFi",
//       "Power Outlets",
//       "Vegan Options",
//       "Outdoor Seating",
//       "Work-Friendly",
//       "Air Conditioning",
//     ],
//     reviews: [
//       {
//         name: "Rhea Choudhury",
//         date: "3 weeks ago",
//         rating: 5,
//         text: "I can't get enough of their cappuccino! The perfect blend of strong coffee and frothy milk.",
//         helpfulCount: 15,
//       },
//       {
//         name: "Kabir Sen",
//         date: "6 days ago",
//         rating: 4.4,
//         text: "The staff here are so attentive and kind! The ambiance is great, and their iced coffee is super refreshing.",
//         helpfulCount: 8,
//       },
//       {
//         name: "Nisha Sharma",
//         date: "1 week ago",
//         rating: 4.5,
//         text: "A gem of a café! The pastries are fresh, and their latte art is beautiful. A must-visit spot!",
//         helpfulCount: 9,
//       },
//       // Add more reviews
//     ],
//     nearbyCafes: [
//       {
//         id: 12,
//         distance: "0.5 km away",
//         shortDescription:
//           "A comfortable cafe with quality drinks and snacks with a friendly atmosphere.",
//       },
//       {
//         id: 19,
//         distance: "0.8 km away",
//         shortDescription:
//           "Enjoy a wide selection of coffee, teas, and light bites.",
//       },
//       {
//         id: 20,
//         distance: "1.2 km away",
//         shortDescription:
//           "Your neighborhood spot for great coffee and a relaxed vibe.",
//       },
//     ], // IDs of nearby cafes
//   },
//   // Add more cafes as needed
// };
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