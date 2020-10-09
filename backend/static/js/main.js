//
// TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
//

// check/uncheck checkboxes in a table
$(".check-all-table").click(function (e) {
    $this = this;  
    $.each($(this).parents('table').find('input'), function(i, item){
        $(item).prop('checked', $this.checked);
    });
});

// the name of the file appear on select
$(".custom-file-input").on("change", function() {
    var fileName = $(this).val().split("\\").pop();
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});

$(".dropdown-item").click(function (e) {
    $this = this;
    var number = $(this).attr('name');
    var dropdown_with_input = $(this).closest('.dropdown-with-input');
    dropdown_with_input.find('input').val(number);
});

