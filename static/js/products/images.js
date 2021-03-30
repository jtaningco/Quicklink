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
    console.log(count);
}

fileBrowse.addEventListener('click', function() {
    openInput();
});

$(":input:file").each(function() {
    $(this).change(function() {
        if ($(this).attr("id") == "id_image_set-0-image") {
            var file_name = String(fileInput0.value).split("\\")[2];
            document.getElementById("js-primary-image").innerHTML = `<div class='product-form-label'><p class='subtitle'>Display Image: <span class='upload__link subtitle'>${file_name}</span>`
            $("#js-primary-image").click(function(){ fileInput0.click(); })
        } else if ($(this).attr("id") == "id_image_set-1-image" || $(this).attr("id") == "id_image_set-2-image") {
            var file_name = String(fileInput1.value).split("\\")[2];
            var file_name_2 = String(fileInput2.value).split("\\")[2];
            document.getElementById("js-other-images").innerHTML = `<p class='subtitle'>Other Images:</p><span class='upload__link subtitle'>${file_name}</span><span class='upload__link subtitle'>${file_name_2}</span>`
            $("#js-primary-image").click(function(){ fileInput1.click(); })
        }
    });
});

$("#id_image_set-0-image").change(function() {
    
});

$("#id_image_set-1-image").change(function() {
    var file_name = String(fileInput0.value).split("\\")[2];
    document.getElementById("js-other-images").innerHTML = "Display Image: <span class='upload__link subtitle'>" + file_name + "</span>"
    $("#js-primary-image").click(function(){ fileInput0.click(); })
});