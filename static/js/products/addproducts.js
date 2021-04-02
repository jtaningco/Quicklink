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
const madeToOrderRadio = document.getElementById('id_made_to_order');
const stocksInputRadio = document.getElementById('stocks-input-select');
const stocksInput = document.getElementById('id_stock');

// Clicking on Made to Order Radio
$('#id_made_to_order').click(function() {
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
const noLimitsRadio = document.getElementById('id_no_order_limit');
const maxOrdersRadio = document.getElementById('orders-input-select');
const maxOrdersInput = document.getElementById('id_orders');

// Clicking on No Order Limits Radio
$('#id_no_order_limit').click(function() {
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
    editPreview();
});

$(":input:file").change(function() {
    canChangeColor();
    editPreview();
});

$(":input:radio").change(function() {
    canChangeColor();
    editPreview();
});

function canChangeColor(index){          
    var can = true;

    if ($("#id_name").val()=='' && $("#id_description").val()=='') {
        can = false
    } else if ($("#id_size_set-0-size").val()=='' && $("#id_size_set-0-price_size").val()=='') {
        can = false 
    } else if (!$("#id_made_to_order").is(':checked')) {
        if ($("#stocks-input-select").is(':checked')) {
            can = true
        } else {
            can = false
        }
    } else if (!$("#id_no_order_limit").is(':checked')) {
        if ($("#orders-input-select").is(':checked')) {
            can = true
        } else {
            can = false
        }
    } else if ($("#orders-input-select").is(':checked') && $("id_orders").val() == '') {
        can = false
    }
    
    if (can) {
        $('#js-preview-product-btn').toggleClass('disabled', false)
    } else {
        $('#js-preview-product-btn').toggleClass('disabled', true)
    }
}

const productHeader = document.getElementById("js-product-header");
const productName = document.getElementById("js-product-name");
const productDescription = document.getElementById("js-product-description");
const productStocks = document.getElementById("js-product-stocks");
const productInstructions = document.getElementById("js-product-instructions");
const productSizes = document.getElementById("js-product-sizes");
const includeAddons = document.getElementById("js-toggle-product-addons");
const productAddons = document.getElementById("js-product-addons");

function editPreview() {
    if ($("#id_name").val() == "") {
        productHeader.innerHTML = "Unnamed Product";
    } else {
        productHeader.innerHTML = $("#id_name").val();
    }

    productName.innerHTML = $("#id_name").val();
    productDescription.innerHTML = $("#id_description").val();

    if ($("#id_made_to_order").is(":checked")) {
        productStocks.innerHTML = "Made to Order"
    } else {
        var stocks = $("#id_stock").val();
        productStocks.innerHTML = `${stocks} stocks remaining`
    }

    if ($("#id_instructions").val()) {
        var instructions = $("#id_instructions").val();
        productInstructions.innerHTML = `Possible Allergens: ${instructions}`
        $("#js-product-instructions").css("display", "flex");
    }
}

function addSizesToPreview() {
    const sizeInputs = $('.js-size-input');
    var sizeList = [];

    sizeInputs.each(function(index) {
        var sizeInput = $(this).val();
        var sizePriceInput = $('.js-size-price-input').eq(index).val();
        const sizeHTML = `<div class="modal__card__content--row"><label class="radio-mobile"><input type="radio"><span class="radio-select-mobile"></span></label><p>${String(sizeInput)} (PHP ${String(sizePriceInput)})</p></div>`
        
        if ($(this).val() != "" || $('.js-size-price-input').eq(index).val() != "") {
            sizeList.push(sizeHTML);
        }
    });

    productSizes.innerHTML = sizeList.join("")
}

function addAddonsToPreview() {
    const addonInputs = $('.js-addon-input');
    var addonList = [];

    addonInputs.each(function(index) {
        var addonInput = $(this).val();
        var addonPriceInput = $(".js-addon-price-input").eq(index).val();
        const addonHTML = `<div class="modal__card__content--row"><label class="checkbox-mobile"><input type="checkbox"><span class="checkmark-mobile"></span></label><p>${String(addonInput)} <span style="color: var(--muted-lighter);">(+ PHP ${String(addonPriceInput)})</span></p></div>`
        
        if ($(this).val() != "" || $('.js-addon-price-input').eq(index).val() != "") {
            addonList.push(addonHTML);
        }
    });

    if (addonList.length > 0) {
        $("#js-toggle-product-addons").css("display", "flex");
        productAddons.innerHTML = addonList.join("")
    }
}

function modalAppear() {
    $("body").css("overflow-y", "hidden");
    $("#js-preview-product-modal").css("display", "flex");
    $("#js-preview-product-modal").css("opacity", "1");
}

function modalExit() {
    $("body").css("overflow-y", "auto");
    $("#js-preview-product-modal").css("display", "none");
    $("#js-preview-product-modal").css("opacity", "0");
}

function initializeSlider() {
    loadImages(fileInput0.files[0], fileInput1.files[0], fileInput2.files[0]);
    $('#js-image-slider').slick({
        dots: true,
        infinite: false,
        speed: 400,
        fade: true,
        cssEase: 'linear',
        autoplay: true,
        autoplaySpeed: 4000,
        adaptiveHeight: false
    });
}

window.onload = function() {
    stocksInput.disabled = true;
    maxOrdersInput.disabled = true;
    $("#sizeForm-TOTAL_SIZES").val($(".size-formset").length);
    $("#addonForm-TOTAL_SIZES").val($(".addon-formset").length);

    $(".size-formset").find("i").first().css("display", "none");
    $(".addon-formset").find("i").first().css("display", "none");

    $("#js-preview-product-btn").click(function() {
        addSizesToPreview();
        addAddonsToPreview();
        modalAppear();
        initializeSlider();
    });

    $(".js-exit-modal").each(function() {
        $(this).click(function() {
            modalExit();
            $('#js-image-slider').slick('unslick');
        });
    });
}