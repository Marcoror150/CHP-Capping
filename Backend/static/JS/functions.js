function previewFilePath() {
    var path = $("#path").val();
    $("#showPath").val(path.split("\\")[2])
    $("#upload").removeAttr('disabled')
}

function changeVal(id, text) {
    $("#" + id).val(text)
}