$(document).ready(function () {
    $(document).on('show.uk.offcanvas', function () {
        $('.filters-offset').css('margin-left', '0');
    });

    $(document).on('hide.uk.offcanvas', function () {
        $('.filters-offset').css('margin-left', '260px');
    });
});