window.onload = function() {
    const form = document.getElementById('my-form');
    const btn = document.getElementById('confirmButton');
    const status = document.getElementById('confirm');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        btn.style.backgroundColor= "var(--secondary-alt)";
        status.innerHTML = 'Sending...';

        const serviceID = 'service_9bg2adh';
        const templateID = 'template_v0jhtg5';

        emailjs.sendForm(serviceID, templateID, this)
            .then(function() {
                form.reset();
                btn.style.backgroundColor = "var(--success-alt)";
                status.innerHTML = "Request sent! We’ll get back to you soon.";
                setTimeout(location.reload(), 500)
            }, function(err) {
                console.log('FAILED...', err);
                btn.style.backgroundColor = "var(--failure-main)";
                status.innerHTML = "Oops! There was a problem. Please try again later.";
            });
    });
}