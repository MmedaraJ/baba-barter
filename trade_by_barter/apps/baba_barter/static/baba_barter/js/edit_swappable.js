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

var images = document.getElementsByClassName("swappable_image");
$(document).ready(function(){
    $('#cancel').on("click", function(){
        history.back();
        return false;
    });
    $('.swappable_image').click(function(){
        if($(this).css("border-style") == "solid"){
            $(this).css("border-style", "none");
            var del = false;
            for(var i=0; i<images.length; i++){
                if(images[i].style.borderStyle == "solid"){
                    del = true;
                }
            }
            if(del == false){
                $('#image_action').toggle("fast", function(){
                    $('#image_action').hide();
                })
            }
        }
        else{
            $(this).css("border-style", "solid");
            var count = 0;
            for(var i=0; i<images.length; i++){
                if(images[i].style.borderStyle == "solid"){
                    count++;
                }
            }
            if(count == 1){
                $('#image_action').toggle("fast", function(){
                    $('#image_action').css("display", "flex");
                });
            }
        }
    });
    $('#type').on("change", function(){
        if($(this).val() == "service"){
            $('#condition_label').hide();
            $('#condition_range').hide();
        }
        else{
            $('#condition_label').show();
            $('#condition_range').show();
        }
    });
    var selected_images = [];
    $('#delete').on("click", function(){
        for(var i=0; i<images.length; i++){
            if(images[i].style.borderStyle == "solid"){
                selected_images.push(images[i].id);
                images[i].parentElement.style.display = "none";
            }
        }
        return false;
    });
    $('#cancel_delete').on("click", function(){
        for(var i=0; i<selected_images.length; i++){
            image = document.getElementById(selected_images[i]);
            image.style.borderStyle = "none";
            image.parentElement.style.display = "inline-block";
        }
        return false;
    });
    $('#save').on("click", function(){
        $.ajaxSetup({async: false});
        data = {}
        for(var i=0; i<selected_images.length; i++){
            data[i] = selected_images[i];
        }
        if(selected_images.length>0){
            $.post("delete/images/", data, function(response){
                if(response == True){

                }
            });
        }
    });
});