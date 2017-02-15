$(document).ready(function() {
    $('.persons--container input').change(function() {
        $(this).parent().toggleClass('hollow');
    });
});
