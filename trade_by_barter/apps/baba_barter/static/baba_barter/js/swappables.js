// Burger menus
document.addEventListener('DOMContentLoaded', function() {
    // open
    const burger = document.querySelectorAll('.navbar-burger');
    const menu = document.querySelectorAll('.navbar-menu');

    if (burger.length && menu.length) {
        for (var i = 0; i < burger.length; i++) {
            burger[i].addEventListener('click', function() {
                for (var j = 0; j < menu.length; j++) {
                    menu[j].classList.toggle('d-none');
                }
            });
        }
    }

    // close
    const close = document.querySelectorAll('.navbar-close');
    const backdrop = document.querySelectorAll('.navbar-backdrop');

    if (close.length) {
        for (var i = 0; i < close.length; i++) {
            close[i].addEventListener('click', function() {
                for (var j = 0; j < menu.length; j++) {
                    menu[j].classList.toggle('d-none');
                }
            });
        }
    }

    if (backdrop.length) {
        for (var i = 0; i < backdrop.length; i++) {
            backdrop[i].addEventListener('click', function() {
                for (var j = 0; j < menu.length; j++) {
                    menu[j].classList.toggle('d-none');
                }
            });
        }
    }
});

function filterSwappables(){
    $.ajax({
        method: $('#filter_swappables_form').attr('method'),
        url: $('#filter_swappables_form').attr('action'),
        data: $('#filter_swappables_form').serialize(),
        success: function(response){
            console.log(response);
            $('#placeholder').html(response)
        }
    });
    return false;
}

$(document).ready(function(){
    $('select[name=category_sort], select[name=order_sort], input[name=value]').on("change", function(){
        filterSwappables();
    });
    $('#location').on("keyup", function(){
        filterSwappables();
    });
});
