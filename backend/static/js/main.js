// check/uncheck checkboxes in a table
$(".check-all-table").click(function (e) {
    $this = this;  
    $.each($(this).parents('table').find('input'), function(i, item){
        $(item).prop('checked', $this.checked);
    });
});

// request to delete Indexes
$("#delIndex").click(function (e) {
    $("#delIndexForm").trigger('click');
});

// request to delete Smarts
$("#delSmart").click(function (e) {
    $("#delSmartForm").trigger('click');
});

// the name of the file appear on select
$(".custom-file-input").on("change", function() {
  var fileName = $(this).val().split("\\").pop();
  $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});

