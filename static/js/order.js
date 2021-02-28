// Size Radio Variables
// const sizeInputs = document.getElementsByClassName('sizeRadio');
// const sizeRadios = document.getElementsByClassName('size-radio-input');
// const sizeLabels = document.getElementsByClassName('product-size');

// Change radio attributes after DOMContent has been loaded
$(document).ready(function() {

    let sizeFormRadioCount = 1;
    $('.size-radio-input').each(function() {
        var name = $(this).attr('name').replace('0', sizeFormRadioCount);
        var id = name;
        $(this).attr({'name': name, 'id': id});
        sizeFormRadioCount++;
    });

    let sizeFormLabelCount = 1;
    $('.product-size').each(function() {
        var newFor = $(this).attr('for').replace('0', sizeFormLabelCount);
        $(this).attr('for', newFor);
        sizeFormLabelCount++;
    });

    let addonFormRadioCount = 1;
    $('.addon-radio-input').each(function() {
        var name = $(this).attr('name').replace('0', addonFormRadioCount);
        var id = name;
        $(this).attr({'name': name, 'id': id});
        addonFormRadioCount++;
    });

    let addonFormLabelCount = 1;
    $('.product-addon').each(function() {
        var newFor = $(this).attr('for').replace('0', addonFormLabelCount);
        $(this).attr('for', newFor);
        addonFormLabelCount++;
    });
})

// Change radio name and id to size_selected when clicked
$('.size-radio-input').click(function() {
    // Get order variables of clicked radio
    var id = $(this).attr('id');
    var id_split = id.split('_')
    var order = id_split[1];
    let sizeFormRadioCount = 1;
    let sizeFormLabelCount = 1;

    // Reset radio attributes of unselected radio
    $('.size-radio-input').each(function() {
        var name = $(this).attr('name').replace('size_selected', 'size_' + sizeFormRadioCount);
        var id = name;
        $(this).attr({'name': name, 'id': id});
        $(this).prop('checked', false);
        sizeFormRadioCount++;
    });

    // Reset label attributes of unselected radio
    $('.product-size').each(function() {
        var newFor = $(this).attr('for').replace('size_selected', 'size_' + sizeFormLabelCount);
        $(this).attr('for', newFor);
        sizeFormLabelCount++;
        if ((sizeFormLabelCount-1) == order) {
            var newFor = $(this).attr('for').replace('size_' + (sizeFormLabelCount - 1), 'size_selected');
            $(this).attr('for', newFor);
        }
    });


    // Turn selected radio into selected_size
    $(this).prop('checked', true);
    var nameSelected = $(this).attr('name').replace('size_' + order, 'size_selected');
    var idSelected = $(this).attr('id').replace('size_' + order, 'size_selected');
    $(this).attr({'name': nameSelected, 'id': idSelected});
})