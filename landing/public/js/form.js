function validateForm() {
    var isValid = true;
    $('.form-field').filter('[required]').each(function() {
        if( $(this).val() === '' ) {
            $('#confirm').prop('enabled', false)
            isValid = false;
        }
    });
    if(isValid) {$('#confirm').prop('enabled', true)}
    return isValid;
}

$('#confirm').click(function() {
    alert(validateForm());
});

// Enable or disable button based on if inputs are filled or not
$('.form-field').filter('[required]').on('keyup',function() {
    validateForm()
    if ($('#confirm').prop('enabled')) {
        $('#confirm').toggleClass('disabled')
        $('#confirmButton').toggleClass('disabled')
    }
});

console.log(validateForm())