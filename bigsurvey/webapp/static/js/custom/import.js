var excel_fields_selector = 'select[name*="excel_field"]';
var unselected_fields_selector = '.unselected-fields';
var example_rows_table = '.example-rows-table';


var selectChangedTrigger = function (select) {
    var val = select.val();
    var prev_val = select.data('previous');
    $(unselected_fields_selector).find('li[data-value="' + prev_val + '"]').show();
    $(example_rows_table).find('th[data-value="' + prev_val + '"]')
        .find('.model_field')
        .removeClass('uk-text-success')
        .addClass('uk-text-danger')
        .text('(None)');
    if (val !== '') {
        $(unselected_fields_selector).find('li[data-value="' + val + '"]').hide();
        $(excel_fields_selector).not(select).filter(function () {
            return $(this).val() === val;
        }).val('').data('previous', '');
        var model_field = select.parent('td').prev().find('input').val();
        $(example_rows_table).find('th[data-value="' + val + '"]')
            .find('.model_field')
            .removeClass('uk-text-danger')
            .addClass('uk-text-success')
            .text(model_field);
    }
    select.data('previous', val);
};

var resetMappings = function () {
    $(excel_fields_selector).val('');
    $(unselected_fields_selector).find('li').show();
    $(example_rows_table).find('th')
        .find('.model_field')
        .removeClass('uk-text-success')
        .addClass('uk-text-danger')
        .text(none_text);
};

var populateMappings = function () {
    if (cached_mappings) {
        for (var key in cached_mappings) {
            if (cached_mappings.hasOwnProperty(key)) {
                var val = cached_mappings[key];
                var select = $('input[value="' + key + '"]').parent('td').next().find(excel_fields_selector);
                select.val(val);
                selectChangedTrigger(select);
            }
        }
    }
};

$(document).ready(function () {
    $(excel_fields_selector).data('previous', $(this).val());

    $(excel_fields_selector).change(function () {
        selectChangedTrigger($(this));
    });

    $('button[data-action="reset"]').click(function () {
        resetMappings();
    });

    $('button[data-action="populate"]').click(function () {
        resetMappings();
        populateMappings();
    });

    populateMappings();
});