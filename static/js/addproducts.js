const form = document.getElementById('product-form');
form.addEventListener("change", () => {
    document.getElementById('submitBtn').disabled = !form.checkValidity()
});
