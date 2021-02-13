window.onload = function() {
    // MOBILE NAVBAR
    var burger = document.getElementById("navBurger");
    
    burger.addEventListener("click", () => {
        document.getElementById("navBurger").classList.toggle("open");
        document.getElementById("openMobileNav").classList.toggle("navbarActive");
        document.getElementById("burgerLines").style.backgroundColor("white");
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
            navOptions[i].style.color = "var(--muted-lighter)";
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
            if (window.matchMedia("(min-width: 960px)").matches) {
                navOptions[i].style.color = "#FFF";
            } else {
                navOptions[i].style.color = "var(--muted-lighter)";
            }
        };
    }
};

window.onbeforeunload = function () {
    window.scrollTo(0, 0);
}