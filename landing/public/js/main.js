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
    } else {
        document.getElementById("navbar").classList.remove("scrolled");
    }
};

window.onbeforeunload = function () {
    window.scrollTo(0, 0);
}