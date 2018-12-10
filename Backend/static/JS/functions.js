// Function to update the path preview when a file to upload is selected
function previewFilePath() {
    var path = $("#path").val();
    $("#showPath").val(path.split("\\")[2])
    $("#upload").removeAttr('disabled')
}

// Function to change the value inside a textbox
function changeVal(id, text) {
    $("#" + id).val(text)
}

// Loads the calendar tool on the ReportPage
function loadDateRange(){
    // Default start and end dates
    var start = moment();
    var end = moment();

    // Callback to insert text in the box when dates are chosen
    function cb(start, end) {
        $('#daterange span').html(start.format('MM/DD/YYYY') + ' to ' + end.format('MM/DD/YYYY'));
    }

    // Activates the calendar tool
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

// Toggles disabled/enabled given a textbox ID
function toggleInput(ID) {
    let checkbox = document.getElementById(ID);

    if(checkbox.checked) {
        $(`#${ID.split('-')[0]}`).prop('disabled',false).selectpicker('refresh');
    } else {
        $(`#${ID.split('-')[0]}`).prop('disabled',true).selectpicker('refresh');
    }
}

// Enables/Disables the calendar tool on click of the checkbox
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

// Enables/Disables the filename textbox on click of the checkbox 
function toggleFilename() {
    let checkbox = document.getElementById('fileBox');

    if(checkbox.checked) {
        $('#filename').prop('disabled', false);
    } else {
        $('#filename').prop('disabled', true);
        $('#filename').val('');
    }
}

// Gets the id of the confirmDeletion button
function getButtonID(ID) {
	$("#confirmDeletion").prop('id', '#' + ID);
}	

// Sets a listener to dynamically update the KID depending on the chosen program on the reports page
function setKIDListener(port){
    $("#program").on("changed.bs.select", function() {
        program = $('#program option:selected').text()
        ip = `http://127.0.0.1${port}/getChildrenProgram/${program}`
    
        $.getJSON(ip, function(data, status) {
            if (status === "success") {
                for(var key in data) {
                    $('#kid').append(`<option>${data[key]}</option>`).selectpicker('refresh');
                }
            }
        });
    });
}

// Inserts the programs that have children enrolled in them on the reports page
function setPrograms(){
    $("#program").on("changed.bs.select", function() {
        program = $('#program option:selected').text()
        ip = `http://127.0.0.1:8076/getChildrenProgram/${program}`
    
        $.getJSON(ip, function(data, status) {
            if (status === "success") {
                for(var key in data) {
                    $('#kid').append(`<option>${data[key]}</option>`).selectpicker('refresh');;
                }
            }
        });
    });
}

// Sets the default text for the upload textbox
function setRecordUpload() {
    changeVal('showPath','Browse to choose file');
    $("#upload").attr( "disabled", "disabled" );
}















