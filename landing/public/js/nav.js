window.onload = function() {
    // MOBILE NAVBAR
    var burger = document.getElementById("navBurger");
    console.log(burger);
    
    burger.addEventListener("click", () => {
        console.log("success");
        document.getElementById("navBurger").classList.toggle("open");
        document.getElementById("openMobileNav").classList.toggle("navbarActive");
    });
}