$(document).ready(function(){
    $('.logout').on("click", function(){
        $('.logoutModal').modal('toggle');
        return false;
    });
    $('.logoutModal').on('shown.bs.modal', function(event){
        $('.yes').on('click', function(){
            $('.yes').attr("href", $('.logout').attr("href"));
        });
        $('.close, .no').on("click", function(){
            $('.logoutModal').modal('hide');
        });
    });
})