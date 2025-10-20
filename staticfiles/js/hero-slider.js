/**
 * Hero Slider
 * Manages the hero background image slider on the home page
 */

document.addEventListener('DOMContentLoaded', function() {
  const slider = document.querySelector('.hero-slider');

  if (!slider) return; // Exit if no slider on page

  const slides = slider.querySelectorAll('.hero-slide');
  const dots = document.querySelectorAll('.slider-dot');

  if (slides.length <= 1) return; // No need for slider logic if only one slide

  let currentSlide = 0;
  let slideInterval;

  /**
   * Show a specific slide
   */
  function showSlide(index) {
    // Remove active class from all slides and dots
    slides.forEach(slide => slide.classList.remove('active'));
    dots.forEach(dot => dot.classList.remove('active'));

    // Add active class to current slide and dot
    slides[index].classList.add('active');
    if (dots[index]) {
      dots[index].classList.add('active');
    }

    currentSlide = index;
  }

  /**
   * Go to next slide
   */
  function nextSlide() {
    const next = (currentSlide + 1) % slides.length;
    showSlide(next);
  }

  /**
   * Go to previous slide
   */
  function prevSlide() {
    const prev = (currentSlide - 1 + slides.length) % slides.length;
    showSlide(prev);
  }

  /**
   * Start auto-play
   */
  function startAutoPlay() {
    stopAutoPlay(); // Clear any existing interval
    slideInterval = setInterval(nextSlide, 5000); // Change slide every 5 seconds
  }

  /**
   * Stop auto-play
   */
  function stopAutoPlay() {
    if (slideInterval) {
      clearInterval(slideInterval);
    }
  }

  /**
   * Handle dot click
   */
  dots.forEach((dot, index) => {
    dot.addEventListener('click', function() {
      showSlide(index);
      stopAutoPlay();
      startAutoPlay(); // Restart auto-play after manual navigation
    });
  });

  /**
   * Pause auto-play on hover (better UX)
   */
  slider.addEventListener('mouseenter', stopAutoPlay);
  slider.addEventListener('mouseleave', startAutoPlay);

  /**
   * Keyboard navigation
   */
  document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowLeft') {
      prevSlide();
      stopAutoPlay();
      startAutoPlay();
    } else if (e.key === 'ArrowRight') {
      nextSlide();
      stopAutoPlay();
      startAutoPlay();
    }
  });

  /**
   * Touch/Swipe support for mobile
   */
  let touchStartX = 0;
  let touchEndX = 0;

  slider.addEventListener('touchstart', function(e) {
    touchStartX = e.changedTouches[0].screenX;
  }, false);

  slider.addEventListener('touchend', function(e) {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
  }, false);

  function handleSwipe() {
    const swipeThreshold = 50; // Minimum swipe distance

    if (touchEndX < touchStartX - swipeThreshold) {
      // Swiped left - go to next slide
      nextSlide();
      stopAutoPlay();
      startAutoPlay();
    }

    if (touchEndX > touchStartX + swipeThreshold) {
      // Swiped right - go to previous slide
      prevSlide();
      stopAutoPlay();
      startAutoPlay();
    }
  }

  // Start auto-play on page load
  startAutoPlay();

  // Pause auto-play when page is not visible
  document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
      stopAutoPlay();
    } else {
      startAutoPlay();
    }
  });
});
