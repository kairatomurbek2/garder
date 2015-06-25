$(document).ready(function () {
    $('input[data-type="non-clickable-checkbox"]').click(function (e) {
        e.preventDefault();
        return false;
    })
});