function previewFilePath() {
    var path = $("#path").val();
    $("#showPath").val(path.split("\\")[2])
    $("#upload").removeAttr('disabled')
}

function changeVal(id, text) {
    $("#" + id).val(text)
}

function loadDateRange(){
    var start = moment();
    var end = moment();

    function cb(start, end) {
        $('#daterange span').html(start.format('MM/DD/YYYY') + ' to ' + end.format('MM/DD/YYYY'));
    }


    $('#daterange').daterangepicker({
        drops: 'down',
        opens: 'center',
        ranges: {
            'Today': [moment(), moment()],
            'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Last 7 Days': [moment().subtract(6, 'days'), moment()],
            'Last 30 Days': [moment().subtract(29, 'days'), moment()],
            'This Month': [moment().startOf('month'), moment().endOf('month')],
            'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        },
        locale: { 
            'separator': " to ",
            'format': 'MM/DD/YYYY'
        },
        alwaysShowCalendars: true,
        autoUpdateInput:true,
    }, cb);

    cb(start, end);
}

function toggleInput(ID) {
    let checkbox = document.getElementById(ID);

    if(checkbox.checked) {
        $(`#${ID.split('-')[0]}`).prop('disabled',false).selectpicker('refresh');
    } else {
        $(`#${ID.split('-')[0]}`).prop('disabled',true).selectpicker('refresh');
    }
}

function toggleDaterange() {
    let checkbox = document.getElementById('dateBox');

    if(checkbox.checked) {
        $('#daterange').prop('disabled', false);
        loadDateRange()
    } else {
        $('#daterange').data('daterangepicker').remove()
        $('#daterange').prop('disabled', true);
        $('#daterange').val('');
    }
}

function toggleFilename() {
    let checkbox = document.getElementById('fileBox');

    if(checkbox.checked) {
        $('#filename').prop('disabled', false);
    } else {
        $('#filename').prop('disabled', true);
        $('#filename').val('');
    }
}

function getButtonID(ID) {
	$("#confirmDeletion").prop('id', '#' + ID);
}	

function setKIDListener(){
    $("#program").on("changed.bs.select", function() {
        program = $('#program option:selected').text()
        ip = "http://0.0.0.0:8080/getChildrenProgram/" + program
    
        $.getJSON(ip, function(data, status) {
            if (status === "success") {
                for(var key in data) {
                    $('#kid').append(`<option>${data[key]}</option>`).selectpicker('refresh');;
                }
            }
        });
    });
}

function setPrograms(){
    $("#program").on("changed.bs.select", function() {
        program = $('#program option:selected').text()
        ip = "http://0.0.0.0:8080/getChildrenProgram/" + program
    
        $.getJSON(ip, function(data, status) {
            if (status === "success") {
                for(var key in data) {
                    $('#kid').append(`<option>${data[key]}</option>`).selectpicker('refresh');;
                }
            }
        });
    });
}

function setRecordUpload() {
    changeVal('showPath','Browse to choose file');
    $("#upload").attr( "disabled", "disabled" );
}















