function realtimeClock() {
    var rtClock = new Date();

    // Get Date Information
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

    var month = months[rtClock.getMonth()];
    var date = rtClock.getDate();
    var year = rtClock.getFullYear();

    // Get Time Information
    var hours = rtClock.getHours();
    var minutes = rtClock.getMinutes();
    var seconds = rtClock.getSeconds();

    // Adding the AM/PM System
    var amPm = ( hours < 12 ) ? "AM" : "PM";

    // Convert to 12-hour format
    hours = (hours > 12) ? hours - 12 : hours;

    // Pad the hours, minutes, and seconds with leading zeros
    hours = ("0" + hours).slice(-2);
    minutes = ("0" + minutes).slice(-2);
    seconds = ("0" + seconds).slice(-2);

    // Display the clock
    document.getElementById('datetime').innerHTML = 
        month + " " + date + ", " + year + " — " + hours + ":" + minutes + ":" + seconds + " " + amPm;
    var t = setTimeout(realtimeClock, 500);
}