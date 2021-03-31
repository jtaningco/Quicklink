const fileBrowse = document.getElementById('js-browse-files');

const fileInput0 = document.getElementById('id_image_set-0-image');
const fileInput1 = document.getElementById('id_image_set-1-image');
const fileInput2 = document.getElementById('id_image_set-2-image');

var count = 0;
let file;

function openInput() {
    if (fileInput0.files.length == 0) {
        fileInput0.click();
    } else if (fileInput1.files.length == 0) {
        fileInput1.click();
    } else if (fileInput2.files.length == 0) {
        fileInput2.click();
    } else {
        if (count == 0) { fileInput0.click();} 
        else if (count == 1) { fileInput1.click();} 
        else if (count == 2) { fileInput2.click(); }
    }

    if (count == 2) {
        count = 0;
    } else { count += 1; }
}

fileBrowse.addEventListener('click', function() {
    openInput();
});

$(":input:file").each(function() {
    $(this).change(function() {
        if ($(this).attr("id") == "id_image_set-0-image") {
            var file_name = String(fileInput0.value).split("\\")[2];
            document.getElementById("js-primary-image").innerHTML = `<div class='product-form-label'><p class='subtitle'>Display Image: <span class='upload__link subtitle' id='js-default'>${file_name}</span>`
            $("#js-default").click(function(){ fileInput0.click(); })
        } else if ($(this).attr("id") == "id_image_set-1-image" || $(this).attr("id") == "id_image_set-2-image") {
            var file_name_2 = String(fileInput1.value).split("\\")[2];
            var file_name_3 = String(fileInput2.value).split("\\")[2];
            if (file_name_3 == undefined || file_name_3 == null) {
                document.getElementById("js-other-images").innerHTML = `<p class='subtitle'>Other Images:</p><span class='upload__link subtitle' id='js-second-image'>${file_name_2}</span>`
            } else {
                document.getElementById("js-other-images").innerHTML = `<p class='subtitle'>Other Images:</p><span class='upload__link subtitle' id='js-second-image'>${file_name_2}</span><span class='upload__link subtitle' id='js-third-image'>${file_name_3}</span>`
            }
            $("#js-second-image").click(function(){ fileInput1.click(); })
            $("#js-third-image").click(function(){ fileInput2.click(); })
        }
    });
});

const imageSlider = document.getElementById("js-image-slider");

function loadImages(file, file_2, file_3) {
    if (file != undefined || file != null) {
        try {
            var fileURL = (window.URL ? URL : webkitURL).createObjectURL(file);
            let imgTag = `<img src="${fileURL}" alt="" class="modal__card__slider__image">`
            imageSlider.innerHTML = imgTag
        } catch (error) {
            var reader = new FileReader();
            reader.readAsDataURL(file);
            let imgTag = `<img src="${fileURL}" alt="" class="modal__card__slider__image" id="js-first-slider-image">`
            imageSlider.innerHTML = imgTag
            reader.onload = function(e) {
                document.getElementById("js-first-slider-image").src = e.target.result;
            };
        }
        if (file_2 != undefined || file_2 != null) {
            var fileURL = (window.URL ? URL : webkitURL).createObjectURL(file);
            var fileURL2 = (window.URL ? URL : webkitURL).createObjectURL(file_2);
            let imgTag = `<img src="${fileURL}" alt="User uploaded logo" class="modal__card__slider__image"><img src="${fileURL2}" alt="User uploaded logo" class="modal__card__slider__image">`
            imageSlider.innerHTML = imgTag
            if (file_3 != undefined || file_3 != null) {
                var fileURL = (window.URL ? URL : webkitURL).createObjectURL(file);
                var fileURL2 = (window.URL ? URL : webkitURL).createObjectURL(file_2);
                var fileURL3 = (window.URL ? URL : webkitURL).createObjectURL(file_3);
                let imgTag = `<img src="${fileURL}" alt="User uploaded logo" class="modal__card__slider__image"><img src="${fileURL2}" alt="User uploaded logo" class="modal__card__slider__image"><img src="${fileURL3}" alt="User uploaded logo" class="modal__card__slider__image">`
                imageSlider.innerHTML = imgTag
            }
        }
    }
}

const productName = document.getElementById("js-product-name");
const productDescription = document.getElementById("js-product-description");
const productStocks = document.getElementById("js-product-stocks");
const productInstructions = document.getElementById("js-product-instructions");
const productSizes = document.getElementById("js-product-sizes");
const includeAddons = document.getElementById("js-toggle-product-addons");
const productAddons = document.getElementById("js-product-addons");

const sizeInputs = document.getElementsByClassName('js-size-input');
const addonInputs = document.getElementsByClassName('js-addon-input');

$("#js-preview-product-btn").click(function(e) {
    e.preventDefault();
    e.stopPropagation();
    $("#js-preview-product-modal").css("display", "flex");
    loadImages(fileInput0.files[0], fileInput1.files[0], fileInput2.files[0]);
    productName.innerHTML = $("#id_name").val();
    productDescription.innerHTML = $("#id_description").val();

    if ($("#made-to-order").is(":checked")) {
        productStocks.innerHTML = "Made to Order"
    } else {
        var stocks = $("id_stock").val();
        productStocks.innerHTML = `${stocks} stocks remaining`
    }

    if ($("#id_instructions").val() != "" || $("#id_instructions").val() != null || $("#id_instructions").val() != undefined) {
        productInstructions.innerHTML = $("#id_instructions").val();
    }

    var sizeList = []
    var addonList = []

    for (var i = 0; sizeInputs.length; i++) {
        var sizeInput = $(".js-size-input").eq(i).val();
        var sizePriceInput = $(".js-size-price-input").eq(i).val();
        const sizeHTML = `<label class="radio-mobile"><input type="radio"><span class="radio-select-mobile"></span></label><p>${sizeInput} (PHP ${sizePriceInput})</p>`
        sizeList.push(sizeHTML);
    }

    if ($(".js-addon-input").eq(0).val() != "") {
        $("js-toggle-product-addons").css("display", "flex");
        for (var i = 0; addonInputs.length; i++) {
            var addonInput = $(".js-addon-input").eq(i).val();
            var addonPriceInput = $(".js-addon-price-input").eq(i).val();
            const addonHTML = `<label class="checkbox-mobile"><input type="checkbox"><span class="checkmark-mobile"></span></label><p>${addonInput} <span style="color: var(--muted-lighter);">(+ PHP ${addonPriceInput}</span></p>`
            addonList.push(addonHTML);
        }
    }

    productSizes.innerHTML = sizeList.join("")
    addonSizes.innerHTML = addonList.join("")
})