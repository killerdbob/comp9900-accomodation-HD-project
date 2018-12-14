;(function($) {
    "use strict";

    // stick menu function
    var nav_offset_top = $('.nav_custom').offset().top;
    $('.nav_custom').affix({
        offset: {
            top: nav_offset_top,
        }
    }); 
    
    // selectpicker
    $('.selectpicker').selectpicker({

    });

    // Flexslider
    jQuery(document).ready(function(){
        $(window).load(function(){
            $('#carousel').flexslider({
                animation: "slide",
                controlNav: true,
                animationLoop: true,
                slideshow: false,
                itemWidth: 230,
                itemMargin: 25,
                dots: true,
                directionNav:false,
                item:3,
                asNavFor: '#slider' 
            });
            $('#slider').flexslider({
                animation: "slide",
                controlNav: false,
                animationLoop: false,
                slideshow: true,
                directionNav:false,
                sync: "#carousel",
                start: function(slider){
                    $('body').removeClass('loading');
                }
            });
        });
    }); 
    
    //Properties Slider
    $('.properties-slider').owlCarousel({
        loop:true,
        margin:30,
        nav:false,
        items:3, 
        responsive:{
            0:{
                items:1
            },
            600:{
                items:2
            },
            1199:{
                items:3
            },
            1920:{
                item:3,
            }
        }

    });

    
    
    // Testimonials Carousel 
    $('.testimonials-carousel').owlCarousel({
        loop:true,
        margin:40,
        nav:false,
        items:2,
        responsive:{
            0:{
                items:1
            },
            600:{
                items:2
            },
            1199:{
                items:2
            },
            1920:{
                item:2,
            }
        }
    });

    // range
    $(function() {
        $( ".widgets #slider-range" ).slider({
            range: true,
            min: 0,
            max: 27000,
            values: [ 5000, 18000 ],
            slide: function( event, ui ) {
                $( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
            }
        });
        $( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) +
           " - $" + $( "#slider-range" ).slider( "values", 1 ) );
    });
    
    // client_logo
    $('.client_logo_section .client_logo').owlCarousel({
        loop:true,
        margin:130,
        nav:false,
        items:5,
        center:true,
         responsive:{
            0:{
                items:1,
            },
            600:{
                items:3
            },
            1000:{
                items:5
            } 
        } 
    });
    
    // CounterUp
    $('.counter').counterUp({
        delay: 10,
        time: 2500
    });

    
     $(window).load(function() { // makes sure the whole site is loaded
		 $('.loader-xbox').fadeOut(); // will first fade out the loading animation
		 $('#preloader').delay(150).fadeOut('slow'); // will fade out the white DIV that covers the website.
		 $('body').delay(150).css({'overflow':'visible'})
     })
    
})(jQuery)