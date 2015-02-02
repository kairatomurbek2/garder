States = {
    HIDDEN: 'hidden',
    VISIBLE: 'visible'
};

$(document).ready(function () {
    $('td a[data-uk-toggle]').click(function () {
        var state = $(this).attr('data-state');

        if (state == States.HIDDEN) {
            $(this).text($(this).attr('data-hide-text'));
            $(this).attr('data-state', States.VISIBLE);
        } else {
            $(this).text($(this).attr('data-show-text'));
            $(this).attr('data-state', States.HIDDEN);
        }
    });
});