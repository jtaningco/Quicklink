window.onload = function() {
    // MOBILE NAVBAR
    var burger = document.getElementById("navBurger");
    
    burger.addEventListener("click", () => {
        document.getElementById("navBurger").classList.toggle("open");
        document.getElementById("openMobileNav").classList.toggle("navbarActive");
    });
}

// NAVBAR SCROLL
window.onscroll = function() {
    if (document.body.scrollTop > 0 || document.documentElement.scrollTop > 0) {
        document.getElementById("navbar").classList.add("scrolled");
        document.getElementById("navLogo").classList.add("scrolled");

        document.getElementById("navButton").classList.remove("primary-white-btn");
        document.getElementById("navButton-link").classList.remove("primary-white-btn-link");

        document.getElementById("navButton").classList.add("primary-btn");
        document.getElementById("navButton-link").classList.add("primary-btn-link");

        document.getElementById("navBurger").classList.add("scroll");
        
        var navOptions = document.getElementsByClassName("navOptions");
        for(var i = 0, length=navOptions.length; i<length; i++) {
            navOptions[i].classList.add("scrolled");
        };
    } else {
        document.getElementById("navbar").classList.remove("scrolled");
        document.getElementById("navLogo").classList.remove("scrolled");
        
        document.getElementById("navButton").classList.add("primary-white-btn");
        document.getElementById("navButton-link").classList.add("primary-white-btn-link");

        document.getElementById("navButton").classList.remove("primary-btn");
        document.getElementById("navButton-link").classList.remove("primary-btn-link");

        document.getElementById("navBurger").classList.remove("scroll");
        
        var navOptions = document.getElementsByClassName("navOptions");
        for(var i = 0, length=navOptions.length; i<length; i++) {
            // if window is greater than 1024px
            if (window.matchMedia("(min-width: 1025px)").matches) {
                // then make navoptions white text
                navOptions[i].classList.remove("scrolled");
            } else {
                navOptions[i].classList.add("scrolled");
            }
        };
    }
}

// NAVBAR SCROLL MOBILE
window.ontouchmove = function() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("navbar").classList.add("scrolled");
        document.getElementById("navLogo").classList.add("scrolled");

        document.getElementById("navButton").classList.remove("primary-white-btn");
        document.getElementById("navButton-link").classList.remove("primary-white-btn-link");

        document.getElementById("navButton").classList.add("primary-btn");
        document.getElementById("navButton-link").classList.add("primary-btn-link");

        document.getElementById("navBurger").classList.add("scroll");
        
        var navOptions = document.getElementsByClassName("navOptions");
        for(var i = 0, length=navOptions.length; i<length; i++) {
            navOptions[i].classList.add("scrolled");
        };
    } else {
        document.getElementById("navbar").classList.remove("scrolled");
        document.getElementById("navLogo").classList.remove("scrolled");
        
        document.getElementById("navButton").classList.add("primary-white-btn");
        document.getElementById("navButton-link").classList.add("primary-white-btn-link");

        document.getElementById("navButton").classList.remove("primary-btn");
        document.getElementById("navButton-link").classList.remove("primary-btn-link");

        document.getElementById("navBurger").classList.remove("scroll");
        
        var navOptions = document.getElementsByClassName("navOptions");
        for(var i = 0, length=navOptions.length; i<length; i++) {
            // if window is greater than 1024px
            if (window.matchMedia("(min-width: 1025px)").matches) {
                // then make navoptions white text
                navOptions[i].classList.remove("scrolled");
            } else {
                navOptions[i].classList.add("scrolled");
            }
        };
    }
}

// ON RESIZE GET NAV OPTIONS BACK TO WHITE
window.onresize = function() {
    if (document.body.scrollTop === 0 || document.documentElement.scrollTop === 0) {
        var navOptions = document.getElementsByClassName("navOptions");
        for(var i = 0, length=navOptions.length; i<length; i++) {
            if (window.matchMedia("(min-width: 1025px)").matches) {
                navOptions[i].classList.remove("scrolled");
            } else {
                navOptions[i].classList.add("scrolled");
            }
        };
    }
}

window.onbeforeunload = function () {
    window.scrollTo(0, 0);
}

// LAZY LOADING IMAGES
document.addEventListener("DOMContentLoaded", function() {
    var lazyloadImages = document.querySelectorAll("img.lazy");    
    var lazyloadThrottleTimeout;
    
    function lazyload () {
      if(lazyloadThrottleTimeout) {
        clearTimeout(lazyloadThrottleTimeout);
      }    
      
      lazyloadThrottleTimeout = setTimeout(function() {
          var scrollTop = window.pageYOffset;
          lazyloadImages.forEach(function(img) {
              if(img.offsetTop < (window.innerHeight + scrollTop)) {
                img.src = img.dataset.src;
                img.classList.remove('lazy');
              }
          });
          if(lazyloadImages.length == 0) { 
            document.removeEventListener("scroll", lazyload);
            window.removeEventListener("resize", lazyload);
            window.removeEventListener("orientationChange", lazyload);
          }
      }, 20);
    }
    
    document.addEventListener("scroll", lazyload);
    window.addEventListener("ontouchmove", lazyload);
    window.addEventListener("resize", lazyload);
    window.addEventListener("orientationChange", lazyload);
});