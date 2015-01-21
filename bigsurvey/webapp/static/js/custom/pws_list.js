States = {
    HIDDEN: 'hidden',
    EXPANDED: 'expanded'
};

$(document).ready(function () {
    $('a[data-id]').click(function () {
        var id = $(this).attr('data-id');
        var state = $(this).attr('data-state');

        var top_half = $('#top-half-pws' + id);
        var bottom_half = $('#bottom-half-pws' + id);

        if (state == States.HIDDEN) {
            $(this).text($(this).attr('data-hide-text'));
            $(this).attr('data-state', States.EXPANDED);
            top_half.addClass('top-half');
            bottom_half.addClass('bottom-half');
        } else {
            $(this).text($(this).attr('data-expand-text'));
            $(this).attr('data-state', States.HIDDEN);
            top_half.removeClass('top-half');
            bottom_half.removeClass('bottom-half');
        }
    });
});