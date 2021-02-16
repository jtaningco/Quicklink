window.onload = function() {
    const btn = document.getElementById('confirmButton');
    const status = document.getElementById('confirm');

    document.getElementById('my-form').addEventListener('submit', function(event) {
        event.preventDefault();

        btn.style.backgroundColor= "var(--secondary-alt)";
        status.innerHTML = 'Sending...';

        const serviceID = 'service_9bg2adh';
        const templateID = 'template_v0jhtg5';

        // generate a five digit number for the contact_number variable
        this.contact_number.value = Math.random() * 100000 | 0;
        
        // these IDs from the previous steps
        emailjs.sendForm(serviceID, templateID, this)
            .then(function() {
                console.log('SUCCESS!');
                btn.style.backgroundColor = "var(--success-alt)";
                status.innerHTML = "Request sent! We’ll get back to you soon.";
            }, function(err) {
                console.log('FAILED...', err);
                btn.style.backgroundColor = "var(--failure-main)";
                status.innerHTML = "Oops! There was a problem. Please try again later.";
            });
    });
}

// document.addEventListener("submit", function() {
//     // get the form elements defined in your form HTML above
//     var form = document.getElementById("my-form");
//     var button = document.getElementById("confirmButton");
//     var status = document.getElementById("confirm");

//     // Success and Error functions for after the form is submitted
//     function success() {
//         form.reset();
//         button.style.backgroundColor = "var(--success-alt);"
//         status.innerHTML = "Request sent! We’ll get back to you soon.";
//     }

//     function error() {
//         button.style.backgroundColor = "var(--failure-main);"
//         status.innerHTML = "Oops! There was a problem.";
//     }

//     // handle the form submission event
//     form.addEventListener("submit", function(ev) {
//         ev.preventDefault();
//         var data = new FormData(form);
//         ajax(form.method, form.action, data, success, error);
//     });
// });

// // helper function for sending an AJAX request
// function ajax(method, url, data, success, error) {
//     var xhr = new XMLHttpRequest();
//     xhr.open(method, url);
//     xhr.setRequestHeader("Accept", "application/json");
//     xhr.onreadystatechange = function() {
//         if (xhr.readyState !== XMLHttpRequest.DONE) return;
//         if (xhr.status === 200) {
//             success(xhr.response, xhr.responseType);
//         } else {
//             error(xhr.status, xhr.response, xhr.responseType);
//         }
//     };
//     xhr.send(data);
// }