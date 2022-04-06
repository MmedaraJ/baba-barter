function filterOtherSwappables(){
    $.ajax({
        method: $('#filter_swappables_form').attr('method'),
        url: "/filter/compare/swappables/" + $("#holder").data("id"),
        data: $('#filter_swappables_form').serialize(),
        success: function(response){
            $('#placeholder_other').html(response)
        }
    });
    return false;
}
    
$(document).ready(function(){
    $('select[name=category_sort], select[name=order_sort], input[name=value], #location, #name').on("change", function(){
        filterOtherSwappables();
    });
    $('#location, #name').on("keyup", function(){
        filterOtherSwappables();
    });

    $(window).keydown(function(event){
        if(event.keyCode == 13) {
            event.preventDefault();
            return false;
        }
    });
});