const selectAllBtn = $("#js-select-all-products-btn");
const deselectAllBtn = $("#js-deselect-all-products-btn");

const selectBtns = $(".js-select-btn");
const setAsInactiveBtn = $("#js-set-as-inactive-btn");
const deleteSelectedBtn = $("#js-delete-selected-btn");

const openDelModal = $("#js-open-delete-modal");
const exitModalBtns = $(".js-modal-exit-btn");

const toggleBtns = $(".js-switch-btn");

// Changing the header
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

// Change row color of selected products
function changeRowColor(element) {
    if (element.is(":checked")) {
        element.parent().parent().parent().addClass("active");
    } else {
        element.parent().parent().parent().removeClass("active");
    }
}

// Select all products
selectAllBtn.click(function() {
    selectBtns.each(function() {
        $(this).prop("checked", true);
        changeRowColor($(this));
        $("#js-select-all-products-btn").prop("checked", true);
    })
    checkSelected();
});

// Deselect all products
deselectAllBtn.click(function() {
    selectBtns.each(function() {
        $(this).prop("checked", false);
        changeRowColor($(this));
        $("#js-select-all-products-btn").prop("checked", false);
    })
    checkSelected();
})

// Click action on each individual checkbox
selectBtns.each(function() {
    $(this).click(function() {
        checkSelected();
        changeRowColor($(this));
    });
});

// Set as inactive button -- pass data to Django View
setAsInactiveBtn.click(function() {
    var inactiveList = []
    selectBtns.each(function() {
        if ($(this).is(":checked")) {
            var item = $(this).val();
            inactiveList.push(item);
        }
    });
    var inactiveListJson = JSON.stringify(inactiveList)
    var next_url = window.location.href + "set-inactive/"

    $.ajax({
        url: next_url,
        type: "POST",
        data: {'products': inactiveListJson},
        success:function(response){
            console.log("Message data successfully sent.")
        },
        error:function (xhr, textStatus, thrownError){
            console.log("Can't send message data.", xhr, textStatus, thrownError);
        }
    }).then(
        setTimeout(function() {
            location.reload()
        }, 1000)
    );
});

// Set as active toggle buttons -- pass data to Django View
toggleBtns.each(function() {
    $(this).click(function() {
        if ($(this).is(":checked")) {
            var item = $(this).val();
            var next_url = window.location.href + "set-active/"
            $.ajax({
                url: next_url,
                type: "POST",
                data: {'products': item},
                success:function(response){
                    console.log("Message data successfully sent.")
                },
                error:function (xhr, textStatus, thrownError){
                    console.log("Can't send message data.", xhr, textStatus, thrownError);
                }
            });
        }
    })
});

// Open delete selected products modal
openDelModal.click(function() {
    $("#js-delete-products-modal").addClass("show");
    var selected = $(".js-select-btn:checked").length
    document.getElementById("js-delete-text").innerHTML = `Are you sure you want to delete these ${selected} items?`
});

// Exit modal buttons
exitModalBtns.each(function() {
    $(this).click(function() {
        $("#js-delete-products-modal").removeClass("show");
    })
})

// Delete all selected products -- pass data to Django View
deleteSelectedBtn.click(function() {
    var selectedProducts = []
    selectBtns.each(function() {
        if ($(this).is(":checked")) {
            var item = $(this).val();
            selectedProducts.push(item);
        }
    });
    var selectedProductsJson = JSON.stringify(selectedProducts)
    var next_url = window.location.href + "delete-selected/"

    $.ajax({
        url: next_url,
        type: "POST",
        data: {'products': selectedProductsJson},
        success:function(response){
            console.log("Message data successfully sent.")
        },
        error:function (xhr, textStatus, thrownError){
            console.log("Can't send message data.", xhr, textStatus, thrownError);
        }
    }).then(
        setTimeout(function() {
            location.reload()
        }, 1000)
    );
});