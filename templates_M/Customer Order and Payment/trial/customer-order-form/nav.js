window.onload - function () {
    //MOBILE NAV
    var burger = document.getElementById("navBurger");

    burger.addEventListener("click", () => {
        document.getElementById("navBurger").classList.toggle("open");
        document.getElementById("openMobileNav").classList.toggle("navbarActive");

    });
}