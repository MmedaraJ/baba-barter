function filterSwappables(){
    $.ajax({
        method: $('#filter_swappables_form').attr('method'),
        url: "/filter/category/" + $("#holder").data("id"),
        data: $('#filter_swappables_form').serialize(),
        success: function(response){
            $('#placeholder').html(response)
        }
    });
    return false;
}

$(document).ready(function(){
    $('select[name=order_sort], input[name=value]').on("change", function(){
        filterSwappables();
    });
    $('#location, #name').on("keyup", function(){
        filterSwappables();
    });
    $(window).keydown(function(event){
        if(event.keyCode == 13) {
            event.preventDefault();
            return false;
        }
    });
});