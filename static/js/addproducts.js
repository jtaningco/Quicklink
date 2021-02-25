// Main Form Variables
const mainForm = document.getElementById("product-form");

// Size Formset Variables
const sizeForm = document.getElementsByClassName("size-formset");
const stockForm = document.getElementById("stock-form");
const addSizeFormBtn = document.getElementById("add-size");
console.log("sizeForm: ", sizeForm)
console.log("addSizeFormBtn: ", addSizeFormBtn)

const totalSizeForms = document.querySelector("#sizeForm-TOTAL_SIZES");
console.log("totalSizeForms: ", totalSizeForms);

let sizeFormCount = sizeForm.length - 1;
console.log("sizeFormCount: ", sizeFormCount);

// Add Size Formset
addSizeFormBtn.addEventListener("click", function(event) {
    event.preventDefault();

    // Clone a New Form
    const newSizeForm = sizeForm[0].cloneNode(true);
    
    // Create / Update Form Count
    const formRegex = RegExp(`form-(\\d){1}-`, 'g');
    sizeFormCount++;
    console.log(sizeFormCount);

    // Update Form Count Value from the HTML Form
    newSizeForm.innerHTML = newSizeForm.innerHTML.replace(formRegex, `form-${sizeFormCount}-`);
    console.log(newSizeForm);
    
    // Insert New Form before the Submit button
    sizeForm.insertBefore(newSizeForm, stockForm);

    // Update Form Count Value from the HTML Form
    totalSizeForms.setAttribute('value', `${sizeFormCount}`);
    console.log(totalSizeForms);
});


// Deleting Element from Size Formset
mainForm.addEventListener("click", function (event) {
    if (event.target.classList.contains("delete-size-form")) {
        event.preventDefault();
        event.target.parentElement.remove();
        sizeFormCount--;
        totalSizeForms.setAttribute('value', `${formCount + 1}`);
    }
});