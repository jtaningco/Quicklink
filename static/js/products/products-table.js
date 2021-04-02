const selectBtns = $(".js-select-btn");

function checkSelected() {
    if ($(".js-select-btn:checked").length > 0) {
        $("#js-normal-table-header").addClass("hide");
        $("#js-select-products").removeClass("hide");
        document.getElementById("js-selected-input").innerHTML = String($(".js-select-btn:checked").length) + " selected"
    } else {
        $("#js-select-products").addClass("hide");
        $("#js-normal-table-header").removeClass("hide");
    }
}

selectBtns.each(function(index) {
    $(this).click(function() {
        checkSelected();
    })
});