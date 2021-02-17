window.onload = function() {
    // MOBILE NAVBAR
    var burger = document.getElementById("navBurger");
    
    burger.addEventListener("click", () => {
        document.getElementById("navBurger").classList.toggle("open");
        document.getElementById("openMobileNav").classList.toggle("navbarActive");
        document.getElementById("burgerLines").style.backgroundColor("white");
    });
}