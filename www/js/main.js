$(".check-all-table").click(function (e) {
    $this = this;  
    $.each($(this).parents('table').find('input'), function(i, item){
    $(item).prop('checked', $this.checked);
  });
});

