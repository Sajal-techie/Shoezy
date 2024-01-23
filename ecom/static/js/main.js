 AOS.init({
 	duration: 800,
 	easing: 'slide'
 });

(function($) {

	"use strict";

	var isMobile = {
		Android: function() {
			return navigator.userAgent.match(/Android/i);
		},
			BlackBerry: function() {
			return navigator.userAgent.match(/BlackBerry/i);
		},
			iOS: function() {
			return navigator.userAgent.match(/iPhone|iPad|iPod/i);
		},
			Opera: function() {
			return navigator.userAgent.match(/Opera Mini/i);
		},
			Windows: function() {
			return navigator.userAgent.match(/IEMobile/i);
		},
			any: function() {
			return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
		}
	};


	$(window).stellar({
    responsive: true,
    parallaxBackgrounds: true,
    parallaxElements: true,
    horizontalScrolling: false,
    hideDistantElements: false,
    scrollProperty: 'scroll'
  });


	// var fullHeight = function() {

	// 	$('.js-fullheight').css('height', $(window).height());
	// 	$(window).resize(function(){
	// 		$('.js-fullheight').css('height', $(window).height());
	// 	});

	// };
	// fullHeight();

	// loader
	var loader = function() {
		setTimeout(function() { 
			if($('#ftco-loader').length > 0) {
				$('#ftco-loader').removeClass('show');
			}
		}, 1);
	};
	loader();

	// Scrollax
//    $.Scrollax();

// 	var carousel = function() {
// 		$('.home-slider').owlCarousel({
// 	    loop:true,
// 	    autoplay: true,
// 	    margin:0,
// 	    animateOut: 'fadeOut',
// 	    animateIn: 'fadeIn',
// 	    nav:false,
// 	    autoplayHoverPause: false,
// 	    items: 1,
// 	    navText : ["<span class='ion-md-arrow-back'></span>","<span class='ion-chevron-right'></span>"],
// 	    responsive:{
// 	      0:{
// 	        items:1
// 	      },
// 	      600:{
// 	        items:1
// 	      },
// 	      1000:{
// 	        items:1
// 	      }
// 	    }
// 		});
	
	// 	$('.carousel-testimony').owlCarousel({
	// 		center: true,
	// 		loop: true,
	// 		items:1,
	// 		margin: 30,
	// 		stagePadding: 0,
	// 		nav: false,
	// 		navText: ['<span class="ion-ios-arrow-back">', '<span class="ion-ios-arrow-forward">'],
	// 		responsive:{
	// 			0:{
	// 				items: 1
	// 			},
	// 			600:{
	// 				items: 1
	// 			},
	// 			1000:{
	// 				items: 1
	// 			}
	// 		}
	// 	});

	// };
	// carousel();

	$('nav .dropdown').hover(function(){
		var $this = $(this);
		// 	 timer;
		// clearTimeout(timer);
		$this.addClass('show');
		$this.find('> a').attr('aria-expanded', true);
		// $this.find('.dropdown-menu').addClass('animated-fast fadeInUp show');
		$this.find('.dropdown-menu').addClass('show');
	}, function(){
		var $this = $(this);
			// timer;
		// timer = setTimeout(function(){
			$this.removeClass('show');
			$this.find('> a').attr('aria-expanded', false);
			// $this.find('.dropdown-menu').removeClass('animated-fast fadeInUp show');
			$this.find('.dropdown-menu').removeClass('show');
		// }, 100);
	});


	$('#dropdown04').on('show.bs.dropdown', function () {
	  console.log('show');
	});

	scroll
	var scrollWindow = function() {
		$(window).scroll(function(){
			var $w = $(this),
					st = $w.scrollTop(),
					navbar = $('.ftco_navbar'),
					sd = $('.js-scroll-wrap');

			if (st > 150) {
				if ( !navbar.hasClass('scrolled') ) {
					navbar.addClass('scrolled');	
				}
			} 
			if (st < 150) {
				if ( navbar.hasClass('scrolled') ) {
					navbar.removeClass('scrolled sleep');
				}
			} 
			if ( st > 350 ) {
				if ( !navbar.hasClass('awake') ) {
					navbar.addClass('awake');	
				}
				
				if(sd.length > 0) {
					sd.addClass('sleep');
				}
			}
			if ( st < 350 ) {
				if ( navbar.hasClass('awake') ) {
					navbar.removeClass('awake');
					navbar.addClass('sleep');
				}
				if(sd.length > 0) {
					sd.removeClass('sleep');
				}
			}
		});
	};
	scrollWindow();

	
	// var counter = function() {
		
	// 	$('#section-counter').waypoint( function( direction ) {

	// 		if( direction === 'down' && !$(this.element).hasClass('ftco-animated') ) {

	// 			var comma_separator_number_step = $.animateNumber.numberStepFactories.separator(',')
	// 			$('.number').each(function(){
	// 				var $this = $(this),
	// 					num = $this.data('number');
	// 					console.log(num);
	// 				$this.animateNumber(
	// 				  {
	// 				    number: num,
	// 				    numberStep: comma_separator_number_step
	// 				  }, 7000
	// 				);
	// 			});
				
	// 		}

	// 	} , { offset: '95%' } );

	// }
	// counter();

	var contentWayPoint = function() {
		var i = 0;
		$('.ftco-animate').waypoint(function(direction) {
		  if (direction === 'down' && !$(this.element).hasClass('ftco-animated')) {
			i++;
			$(this.element).addClass('item-animate');
			setTimeout(function() {
			  $('body .ftco-animate.item-animate').each(function(k) {
				var el = $(this);
				setTimeout(function() {
				  var effect = el.data('animate-effect');
				  if (effect === 'fadeIn') {
					el.addClass('fadeIn ftco-animated').css('animation-duration', '0.1s');
				  } else if (effect === 'fadeInLeft') {
					el.addClass('fadeInLeft ftco-animated').css('animation-duration', '0.1s');
				  } else if (effect === 'fadeInRight') {
					el.addClass('fadeInRight ftco-animated').css('animation-duration', '0.1s');
				  } else {
					el.addClass('fadeInUp ftco-animated').css('animation-duration', '0.1s');
				  }
				  el.removeClass('item-animate');
				}, k * 1, 'easeInOutExpo');
			  });
			}, 10);
		  }
		}, { offset: '95%' });
	  };
	  contentWayPoint();


	// navigation
	var OnePageNav = function() {
		$(".smoothscroll[href^='#'], #ftco-nav ul li a[href^='#']").on('click', function(e) {
		 	e.preventDefault();

		 	var hash = this.hash,
		 			navToggler = $('.navbar-toggler');
		 	$('html, body').animate({
		    scrollTop: $(hash).offset().top
		  }, 700, 'easeInOutExpo', function(){
		    window.location.hash = hash;
		  });


		  if ( navToggler.is(':visible') ) {
		  	navToggler.click();
		  }
		});
		$('body').on('activate.bs.scrollspy', function () {
		  console.log('nice');
		})
	};
	OnePageNav();


	// magnific popup
// 	$('.image-popup').magnificPopup({
//     type: 'image',
//     closeOnContentClick: true,
//     closeBtnInside: false,
//     fixedContentPos: true,
//     mainClass: 'mfp-no-margins mfp-with-zoom', // class to remove default margin from left and right side
//      gallery: {
//       enabled: true,
//       navigateByImgClick: true,
//       preload: [0,1] // Will preload 0 - before current, and 1 after the current image
//     },
//     image: {
//       verticalFit: true
//     },
//     zoom: {
//       enabled: true,
//       duration: 300 // don't foget to change the duration also in CSS
//     }
//   });

var image = document.getElementById('zoom-image');
var container = document.querySelector('.image-zoom-container');

container.addEventListener('mousemove', function (e) {
    var rect = container.getBoundingClientRect();
    var x = e.clientX - rect.left; // X position within the container
    var y = e.clientY - rect.top; // Y position within the container

    var scaleX = container.offsetWidth / image.naturalWidth;
    var scaleY = container.offsetHeight / image.naturalHeight;

    // Calculate the percentage position within the container
    var percentX = (x / container.offsetWidth) * 100;
    var percentY = (y / container.offsetHeight) * 100;

    // Set the transform origin based on the mouse position
    image.style.transformOrigin = percentX + '% ' + percentY + '%';
});

container.addEventListener('mouseleave', function () {
    // Reset the transform origin when the mouse leaves the container
    image.style.transformOrigin = '0% 0%';
});



	var goHere = function() {

		$('.mouse-icon').on('click', function(event){
			
			event.preventDefault();

			$('html,body').animate({
				scrollTop: $('.goto-here').offset().top
			}, 500, 'easeInOutExpo');
			
			return false;
		});
	};
	goHere();

	// function makeTimer() {

	// 	var endTime = new Date("21 December 2019 9:56:00 GMT+01:00");			
	// 	endTime = (Date.parse(endTime) / 1000);

	// 	var now = new Date();
	// 	now = (Date.parse(now) / 1000);

	// 	var timeLeft = endTime - now;

	// 	var days = Math.floor(timeLeft / 86400); 
	// 	var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
	// 	var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
	// 	var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));

	// 	if (hours < "10") { hours = "0" + hours; }
	// 	if (minutes < "10") { minutes = "0" + minutes; }
	// 	if (seconds < "10") { seconds = "0" + seconds; }

	// 	$("#days").html(days + "<span>Days</span>");
	// 	$("#hours").html(hours + "<span>Hours</span>");
	// 	$("#minutes").html(minutes + "<span>Minutes</span>");
	// 	$("#seconds").html(seconds + "<span>Seconds</span>");		

// }
setInterval(function() { makeTimer(); }, 1000);




})(jQuery);



let timerOn = true;
function timer(remaining) {
  var m = Math.floor(remaining / 60);
  var s = remaining % 60;
  m = m < 10 ? "0" + m : m;
  s = s < 10 ? "0" + s : s;
  document.getElementById("countdown").innerHTML = `Time left: ${m} : ${s}`;
  remaining -= 1;
  if (remaining >= 0 && timerOn) {
    setTimeout(function () {
      timer(remaining);
    }, 1000);
    document.getElementById("resend").innerHTML = `
    `;
    return;
  }
  if (!timerOn) {
    return;
  }
  document.getElementById("resend").innerHTML = `Don't receive the code? 
  <span class="font-weight-bold text-color cursor" onclick="timer(60)">Resend
  </span>`;
}
timer(60);

