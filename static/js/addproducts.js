// Main Form Variables
const mainForm = document.getElementById("product-form");

// Size Formset Variables
const sizeForm = document.getElementsByClassName("size-formset");
const addSizeFormBtn = document.getElementById("add-size");

const totalSizeForms = document.querySelector("#sizeForm-TOTAL_SIZES");
const maxSizeForms = document.querySelector("#sizeForm-MAX_NUM_SIZES");
const minSizeForms = document.querySelector("#sizeForm-MIN_NUM_SIZES");

let sizeFormCount = sizeForm.length;

// Add Size Formset
function addSize(selector, type) {
    var newSizeForm = $(selector).clone(true);
    
    newSizeForm.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (sizeFormCount-1) + '-', '-' + sizeFormCount + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });

    newSizeForm.find('label').each(function() {
        var newFor = $(this).attr('for').replace('-' + (sizeFormCount-1) + '-', '-' + sizeFormCount + '-');
        $(this).attr('for', newFor);
    });

    sizeFormCount++;
    totalSizeForms.setAttribute('value', sizeFormCount);
    $('#id_' + type + '-TOTAL_FORMS').val(sizeFormCount);
    $(selector).after(newSizeForm);
}

$('#add-size').click(function() {
    var max = parseInt($(maxSizeForms).attr('value'));

    if (sizeFormCount < max) {
        addSize('.size-formset:last', 'size_set')
    } else {
        alert("You can't have more than 10 available sizes or servings.");
    }
})


// Deleting Element from Size Formset
mainForm.addEventListener("click", function (event) {
    if (event.target.classList.contains("delete-size-form")) {
        var min = parseInt($(minSizeForms).attr('value'));

        if (sizeFormCount > min) {
            event.preventDefault();
            event.target.parentElement.remove();
            sizeFormCount--;
            totalSizeForms.setAttribute('value', `${sizeFormCount}`);
        } else {
            alert("You can't have less than 1 available size or serving.");
        }
    }
});

// Addon Formset Variables
const addonForm = document.getElementsByClassName("addon-formset");
const addAddonFormBtn = document.getElementById("add-addon");

const totalAddonForms = document.querySelector("#addonForm-TOTAL_SIZES");
const maxAddonForms = document.querySelector("#addonForm-MAX_NUM_SIZES");
const minAddonForms = document.querySelector("#addonForm-MIN_NUM_SIZES");

let addonFormCount = addonForm.length-1;

// Add Addon Formset
function addAddon(selector, type) {
    if (addonFormCount >= 1) {
        var newAddonForm = $(selector).clone(true);
            
        newAddonForm.find(':input').each(function() {
            var name = $(this).attr('name').replace('-' + (addonFormCount-1) + '-', '-' + addonFormCount + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        });
        
        newAddonForm.find('label').each(function() {
            var newFor = $(this).attr('for').replace('-' + (addonFormCount-1) + '-', '-' + addonFormCount + '-');
            $(this).attr('for', newFor);
        });
        
        addonFormCount++;
        totalAddonForms.setAttribute('value', addonFormCount);
        $('#id_' + type + '-TOTAL_FORMS').val(addonFormCount);
        $(selector).after(newAddonForm);
    } else {
        $('.addon-formset').find(':input').each(function() {
            $(this).css('display', 'flex');
        });
        addonFormCount++;
    }
}

$('#add-addon').click(function() {
    var max = parseInt($(maxAddonForms).attr('value'));

    if (addonFormCount < max) {
        addAddon('.addon-formset:last', 'addon_set')
    } else {
        alert("You can't have more than 10 available addons.");
    }
})

// Deleting Element from Addon Formset
mainForm.addEventListener("click", function (event) {
    if (event.target.classList.contains("delete-addon-form")) {
        var min = parseInt($(minAddonForms).attr('value'));

        if (addonFormCount > min) {
            event.preventDefault();
            event.target.parentElement.remove();
            addonFormCount--;
            totalAddonForms.setAttribute('value', `${addonFormCount}`);
        } else {
            $('.addon-formset').find(':input').each(function() {
                $(this).css('display', 'none');
            });
            addonFormCount--;
        }
    }
});

// Stocks Variables
const madeToOrderRadio = document.getElementById('made-to-order');
const stocksInputRadio = document.getElementById('stocks-input-select');
const stocksInput = document.getElementById('id_stock');

// Clicking on Made to Order Radio
$('#made-to-order').click(function() {
    stocksInputRadio.checked = false;

    if ($('#stocks-input-select').is(':checked')) { 
        stocksInput.disabled = false;
        stocksInput.classList.remove('disabled');
    } else {
        stocksInput.disabled = true;
        stocksInput.classList.add('disabled');
    }
})

// Click on Input Radio
$('#stocks-input-select').click(function() {
    madeToOrderRadio.checked = false;

    if ($('#stocks-input-select').is(':checked')) { 
        stocksInput.disabled = false;
        stocksInput.classList.remove('disabled');
    } else {
        stocksInput.disabled = true;
        stocksInput.classList.add('disabled');
    }
 });

// Days Variables
const openDaysRadio = document.getElementById('open-days');
const openDaysInput = document.getElementById('id_days');

$('#open-days').click(function() {
    if ($('#open-days').is(':checked')) { 
        openDaysInput.disabled = false;
        openDaysInput.classList.remove('disabled');
    } else {
        openDaysInput.disabled = true;
        openDaysInput.classList.add('disabled');
    }
});

// Time Variables
const cutoffTimeRadio = document.getElementById('cutoff-time');
const cutoffTimeInput = document.getElementById('id_time');

$('#cutoff-time').click(function() {
    if ($('#cutoff-time').is(':checked')) { 
        cutoffTimeInput.disabled = false;
        cutoffTimeInput.classList.remove('disabled');
    } else {
        cutoffTimeInput.disabled = true;
        cutoffTimeInput.classList.add('disabled');
    }
});

// Maximum Orders Variables
const noLimitsRadio = document.getElementById('no-order-limits');
const maxOrdersRadio = document.getElementById('orders-input-select');
const maxOrdersInput = document.getElementById('id_orders');

// Clicking on No Order Limits Radio
$('#no-order-limits').click(function() {
    maxOrdersRadio.checked = false;

    if ($('#orders-input-select').is(':checked')) { 
        maxOrdersInput.disabled = false;
    } else {
        maxOrdersInput.disabled = true;
    }
})

// Click on Input Radio
$('#orders-input-select').click(function() {
    noLimitsRadio.checked = false;

    if ($('#orders-input-select').is(':checked')) { 
        maxOrdersInput.disabled = false;
        maxOrdersInput.classList.remove('disabled');
    } else {
        maxOrdersInput.disabled = true;
        maxOrdersInput.classList.add('disabled');
    }
 });

window.onload = function() {
    stocksInput.disabled = true;
    openDaysInput.disabled = true;
    maxOrdersInput.disabled = true;

    $('.addon-formset').find(':input').each(function() {
        $(this).css('display', 'none');
    });
}