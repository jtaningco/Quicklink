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

function displayImageInputs(el) {
    if (el.attr("id") == "id_image_set-0-image") {
        var file_name = String(fileInput0.value).split("\\")[2];
        document.getElementById("js-primary-image").innerHTML = `<div class='product-form-label'><p class='subtitle'>Display Image: <span class='upload__link subtitle' id='js-default'>${file_name}</span>`
        $("#id_image_set-0-default").prop('checked', true);
        $("#js-default").click(function(){ fileInput0.click(); })
    } else if (el.attr("id") == "id_image_set-1-image" || el.attr("id") == "id_image_set-2-image") {
        var file_name_2 = String(fileInput1.value).split("\\")[2];
        var file_name_3 = String(fileInput2.value).split("\\")[2];
        if (file_name_3 == undefined || file_name_3 == null) {
            document.getElementById("js-other-images").innerHTML = `<p class='subtitle'>Other Images:</p><span class='upload__link subtitle' id='js-second-image'>${file_name_2}</span>`
        } else {
            document.getElementById("js-other-images").innerHTML = `<p class='subtitle'>Other Images:</p><span class='upload__link subtitle' id='js-second-image'>${file_name_2}</span><span class='upload__link subtitle' id='js-third-image'>${file_name_3}</span>`
            fileBrowse.style.display = "none";
        }
        $("#js-second-image").click(function(){ fileInput1.click(); })
        $("#js-third-image").click(function(){ fileInput2.click(); })
    }
}

$(":input:file").each(function() {
    $(this).change(function() {
        displayImageInputs($(this));
    });
});

const imageSlider = document.getElementById("js-image-slider");

function loadImages(file, file_2, file_3) {
    if (file != undefined || file != null) {
        console.log(file)
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
            console.log(file_2)
            var fileURL = (window.URL ? URL : webkitURL).createObjectURL(file);
            var fileURL2 = (window.URL ? URL : webkitURL).createObjectURL(file_2);
            let imgTag = `<img src="${fileURL}" alt="User uploaded logo" class="modal__card__slider__image"><img src="${fileURL2}" alt="User uploaded logo" class="modal__card__slider__image">`
            imageSlider.innerHTML = imgTag
            if (file_3 != undefined || file_3 != null) {
                console.log(file_3)
                var fileURL = (window.URL ? URL : webkitURL).createObjectURL(file);
                var fileURL2 = (window.URL ? URL : webkitURL).createObjectURL(file_2);
                var fileURL3 = (window.URL ? URL : webkitURL).createObjectURL(file_3);
                let imgTag = `<img src="${fileURL}" alt="User uploaded logo" class="modal__card__slider__image"><img src="${fileURL2}" alt="User uploaded logo" class="modal__card__slider__image"><img src="${fileURL3}" alt="User uploaded logo" class="modal__card__slider__image">`
                imageSlider.innerHTML = imgTag
            }
        }
    }
}

$("#js-preview-product-btn").click(function() {
    loadImages(fileInput0.files[0], fileInput1.files[0], fileInput2.files[0]);
});