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
    //closing now
});

$(document).ready(function(){
    //if edit profile is clicked, replace profile info below with the edit profile form
    $("#edit_profile_link").on("click", function(){
        data = {'id': $("#edit_profile_link").data("id")}
        $.ajax({
            type: "POST",
            url: $("#edit_profile_link").attr("href"),
            data: data,
            success: function(response){
                console.log(response)
                $('#placeholder_edit_and_report').html(response);
                console.log($('#placeholder_edit_and_report').html());
                $('#profile_info').hide("fast");
            }
        });
        return false;
    });

    //if report profile is clicked, replace placeholder div below with the edit profile form
    $("#report_profile_link").on("click", function(){
        data = {'id': $("#report_profile_link").data("id")}
        $.ajax({
            type: "POST",
            url: $("#report_profile_link").attr("href"),
            data: data,
            success: function(response){
                $('#placeholder_edit_and_report').html(response);
            }
        });
        return false;
    });

    $("#update_profile_picture_link").on("click", function(){
        $.ajax({
            type: "POST",
            url: $("#update_profile_picture_link").attr("href"),
            success: function(response){
                $('#profile_picture_edit').html(response);
            }
        });
        return false;
    });
});