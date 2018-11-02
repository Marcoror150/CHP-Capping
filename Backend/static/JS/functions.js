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

function toggleDaterange(){
    let checkbox = document.getElementById('dateBox');

    if(checkbox.checked) {
        $('#daterange').prop('readonly', false);
        loadDateRange()
    } else {
        $('#daterange').data('daterangepicker').remove()
        $('#daterange').prop('readonly', true);
        $('#daterange').val('');
    }
}