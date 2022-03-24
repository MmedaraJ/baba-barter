$(document).ready(function(){
    $('#cancel').on("click", function(){
        $('#edit_profile').hide("fast");
        $('#profile_info').show("fast");
        return false;
    });
});