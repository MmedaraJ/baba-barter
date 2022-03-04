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

//TODO change plus sign to minus sign svg when .show()
var description = false
var notes = false
$(document).ready(function(){
    if(description == false){
        $('#long_description').hide();
    }else{
        $('#long_description').show();
    }
    if(notes == false){
        $('#notes').hide();
    }else{
        $('#notes').show();
    }
    $('#show_description').on("click", function(){
        if(description == false){
            $('#long_description').show();
            description = true
        } else{
            $('#long_description').hide();
            description = false
        }
        return false;
    })
    $('#show_notes').on("click", function(){
        if(description == false){
            $('#notes').show();
            description = true
        } else{
            $('#notes').hide();
            description = false
        }
        return false;
    })
})