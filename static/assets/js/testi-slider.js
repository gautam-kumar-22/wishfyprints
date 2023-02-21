/*--------------- Testimonial Slider ---------------*/ 
var swiper = new Swiper(".testimonial-slider", {

  spaceBetween: 30,
  loop:true,
  autoplay: {
    delay: 5000,
    disableOnInteraction: false, 
  },

  pagination: {
    el: ".swiper-pagination2",
    clickable:true,
  },

  breakpoints: {
    0: {
      slidesPerView: 1,
    },
    768: {
      slidesPerView: 2,
    },
},

}); 
