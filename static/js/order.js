// Size Radio Variables
// const sizeInputs = document.getElementsByClassName('sizeRadio');
// const sizeRadios = document.getElementsByClassName('size-radio-input');
// const sizeLabels = document.getElementsByClassName('product-size');

// Change radio attributes after DOMContent has been loaded
$(document).ready(function() {
    let sizeFormRadioCount = 1;
    $('.size-radio-input').each(function() {
        var id = $(this).attr('id').replace(sizeFormRadioCount-1, sizeFormRadioCount);
        $(this).attr({'id': id});
        sizeFormRadioCount++;
    });

    let sizeFormLabelCount = 1;
    $('.product-size').each(function() {
        var newFor = $(this).attr('for').replace(sizeFormLabelCount-1, sizeFormLabelCount);
        $(this).attr('for', newFor);
        sizeFormLabelCount++;
    });

    let addonFormRadioCount = 1;
    $('.addon-radio-input').each(function() {
        var id = $(this).attr('id').replace(addonFormRadioCount-1, addonFormRadioCount);
        $(this).attr({'id': id});
        addonFormRadioCount++;
    });

    let addonFormLabelCount = 1;
    $('.product-addon').each(function() {
        var newFor = $(this).attr('for').replace(addonFormLabelCount-1, addonFormLabelCount);
        $(this).attr('for', newFor);
        addonFormLabelCount++;
    });

    

    setInterval(function(){
        // Get price of selected size
        var sizeId = $("input[type='radio'][name='size']:checked").attr('id');
        var sizePrice = parseInt($("label[for='" + sizeId + "']").data('price'));
        if (isNaN(sizePrice) == false) {
            var total = sizePrice
        }

        // Get prices of selected addons
        var addonTotal = 0;
        $('.order-product-addon').find("input:checked").each(function() {
            var addonId = $(this).attr('id');
            var addonPrice = parseInt($("label[for='" + addonId + "']").data('price'));
            addonTotal = addonTotal + addonPrice;
        });

        if (isNaN(addonTotal) == false) {
            total = sizePrice + addonTotal
        }

        var quantity = $('#id_quantity').val();
        if (isNaN(quantity) == false) {
            total = (sizePrice + addonTotal) * quantity
        }

        if (isNaN(total)) {
            document.getElementById('add-to-basket').innerHTML = 
            "Add to Basket";
        } else {
            document.getElementById('add-to-basket').innerHTML = 
            "Add to Basket — PHP " + total;
        }
    }, 1000);
})

// Change radio name and id to size_selected when clicked
$('.size-radio-input').click(function() {
    // Reset radio attributes of unselected radio
    $('.size-radio-input').each(function() {
        $(this).prop('checked', false);
    });

    // Turn selected radio into selected_size
    $(this).prop('checked', true);
})