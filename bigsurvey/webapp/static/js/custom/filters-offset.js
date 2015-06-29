$(document).ready(function () {
    var filters = $('.fixed-filters');
    var navbar = $('nav.uk-navbar');
    var navbarHeight = parseInt(navbar.height());
    var navbarWidth = parseInt(navbar.width());
    var paginationWrapper = $('.pagination-wrapper');

    var defaultTop = parseInt(filters.css('top'));
    var lastScrollLeft = 0;
    var documentScrollLeft;

    $('.clickable-row').click(function (e) {
        window.document.location = $(this).data("href");
    });

    $('.fixed-headers').floatThead({
        scrollingTop: navbarHeight
    });

    $(document).scroll(function (e) {
        documentScrollLeft = $(document).scrollLeft();
        if (lastScrollLeft != documentScrollLeft) {
            scrollPagination();
            lastScrollLeft = documentScrollLeft;
        }
    });

    function scrollPagination() {
        paginationWrapper.css('margin-left', documentScrollLeft + 'px');
    }

    $(document).on('show.uk.offcanvas', function () {
        $('.filters-offset').css('margin-left', '0');
    });

    $(document).on('hide.uk.offcanvas', function () {
        $('.filters-offset').css('margin-left', '260px');
    });
});