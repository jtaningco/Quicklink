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

    newSizeForm.find("i").css("display", "flex");

    sizeFormCount++;
    totalSizeForms.setAttribute('value', sizeFormCount);
    $('#id_' + type + '-TOTAL_FORMS').val(sizeFormCount);
    $(selector).after(newSizeForm);
}

$('#add-size').click(function() {
    var max = parseInt($(maxSizeForms).attr('value'));

    if (sizeFormCount < max) {
        addSize('.size-formset:last', 'size_set')
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

        newAddonForm.find("i").css("display", "flex");
        
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

$(".input").on("keyup", function() {    	
    canChangeColor();
});

$(":input:file").change(function() {
    canChangeColor();
});

$(":input:radio").change(function() {
    canChangeColor();
});

function canChangeColor(index){          
    var can = true;

    if ($("#stocks-input-select").is(':checked')) {
        console.log($("#id_stock").val());
    }

    if ($("#id_name").val()=='' && $("#id_description").val()=='') {
        console.log("Name and Description Failed!")
        can = false
    } else if (document.getElementById('id_image_set-0-image').files.length == 0) {
        console.log("Image Failed!")
        can = false 
    } else if ($("#id_size_set-0-size").val()=='' && $("#id_size_set-0-price_size").val()=='') {
        console.log("Sizes Failed!")
        can = false 
    } else if (!$("#made-to-order").is(':checked')) {
        can = false
        if ($("#stocks-input-select").is(':checked') && $("#id_stock").val()!='') {
            can = true
        }
    } else if ($("#stocks-input-select").is(':checked') && $("#id_stock").val()=='') {
        can = false
    } else if (!$("#no-order-limits").is(':checked')) {
        can = false
        if ($("#orders-input-select").is(':checked') && $("#id_orders").val()!='') {
            can = true
        }
    } else if ($("#orders-input-select").is(':checked') && $("id_orders").val()=='') {
        console.log("Orders input selected but input is blank!")
        can = false
    }
    
    if (can) {
        $('#js-preview-product-btn').toggleClass('disabled', false)
    } else {
        $('#js-preview-product-btn').toggleClass('disabled', true)
    }
}

window.onload = function() {
    stocksInput.disabled = true;
    maxOrdersInput.disabled = true;

    $(".size-formset").find("i").first().css("display", "none");
    $(".addon-formset").find("i").first().css("display", "none");
}