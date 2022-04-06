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
    //display the images with a solid border
    $('#display_image').attr("src", images[display_index].src);
    images[display_index].style.borderStyle = "solid";
    
    /*
        When the left arrow is clicked, 
        1. Clear all borders on the other images
        2. Set a border on the previous image (the currently selected image)
        3. Set the currently selected(bordered) image as the main display iimage
    */
    $('#left_scroll').on("click", function(){
        //display_index determines which image to display as the main
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

    /*
        When the right arrow is clicked, 
        1. Clear all borders on the other images
        2. Set a border on the next image (the currently selected image)
        3. Set the currently selected(bordered) image as the main display iimage
    */
    $('#right_scroll').on("click", function(){
        //display_index determines which image to display as the main
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

    /*
        When the show description div is clicked, 
        1. Hide/Show the long_description div 
    */
    $('#show_description').on("click", function(){
        $('#long_description').toggle("slow", function(){
            if($('#long_description').is(":visible")){
                $('#long_description').show();
            } else{
                $('#long_description').hide();
            }
        });
    });

    /*
        When the show notes div is clicked, 
        1. Hide/Show the notes div 
    */
    $('#show_notes').on("click", function(){
        $('#notes').toggle("slow", function(){
            if($('#notes').is(":visible")){
                $('#notes').show();
            } else{
                $('#notes').hide();
            }
        })
    });

    /*
        When one of the small images are clicked,
        1. clear all the other borders
        2. set border on the clicked image
    */
    $('.swappable_image').click(function(){
        $('.swappable_image').css("border-style", "none")
        $(this).css("border", "solid");
        $('#display_image').attr("src", $(this).attr("src"));
        return false;
    });

    /*
        When delete is clicked, 
        1. show the delete modal
    */
    $('#delete').on("click", function(){
        $('#delete_swappable_modal').modal('toggle');
        return false;
    });
    /* 
        1. If yes is clicked, delete the swappable
        2. if no or close are clicked, close the modal and do not delete swappable
    */
    $('#delete_swappable_modal').on('shown.bs.modal', function(event){
        $('#yes').on('click', function(){
            $('#yes').attr("href", $('#delete').attr("href"));
        });
        $('#close, #no').on("click", function(){
            $('#delete_swappable_modal').modal('hide');
        });
    });

    //if report profile is clicked, replace placeholder div below with the edit profile form
    $("#report_profile_link").on("click", function(){
        data = {'id': $("#report_profile_link").data("id")}
        $.ajax({
            type: "POST",
            url: $("#report_profile_link").attr("href"),
            data: data,
            success: function(response){
                $('#placeholder').html(response);
            }
        });
        return false;
    });
});