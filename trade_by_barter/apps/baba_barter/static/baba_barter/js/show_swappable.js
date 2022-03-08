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
var images = document.getElementsByClassName('swappable_image');
function get_display_index(){
    for(var i=0; i<images.length; i++){
        if(images[i].style.borderStyle == "solid"){
            return i;
        }
    }
}

display_index = 0;

$(document).ready(function(){
    $('#display_image').attr("src", images[display_index].src);
    images[display_index].style.borderStyle = "solid";

    $('#left_scroll').on("click", function(){
        display_index = get_display_index();
        if(display_index == 0){
            display_index = images.length - 1;
        } else{
            display_index--;
        }
        $('.swappable_image').css("border-style", "none")
        images[display_index].style.borderStyle = "solid";
        $('#display_image').attr("src", images[display_index].src);
        return false;
    });

    $('#right_scroll').on("click", function(){
        display_index = get_display_index();
        if(display_index == images.length - 1){
            display_index = 0;
        } else{
            display_index++;
        }
        $('.swappable_image').css("border-style", "none")
        images[display_index].style.borderStyle = "solid";
        $('#display_image').attr("src", images[display_index].src);
        return false;
    });

    $('#show_description').on("click", function(){
        $('#long_description').toggle("slow", function(){
            if($('#long_description').is(":visible")){
                $('#long_description').show();
            } else{
                $('#long_description').hide();
            }
        })
    });

    $('#show_notes').on("click", function(){
        $('#notes').toggle("slow", function(){
            if($('#notes').is(":visible")){
                $('#notes').show();
            } else{
                $('#notes').hide();
            }
        })
    });
    
    $('.swappable_image').click(function(){
        $('.swappable_image').css("border-style", "none")
        $(this).css("border", "solid");
        $('#display_image').attr("src", $(this).attr("src"));
        return false;
    });
});