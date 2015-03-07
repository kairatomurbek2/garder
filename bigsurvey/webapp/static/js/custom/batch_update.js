Xpath = {
    global_checkbox: 'input[type="checkbox"][data-action="check_all"]',
    concrete_checkbox: 'input[type="checkbox"][name="site_pks"]'
};
Xpath.concrete_checbox_checked = Xpath.concrete_checkbox + ':checked';

function setAllCheckboxes(state) {
    $(Xpath.concrete_checkbox).prop('checked', state);
}

$(document).ready(function () {
    $(Xpath.global_checkbox).click(function (e) {
        var currentState = $(this).is(':checked');

        setAllCheckboxes(currentState);
    });

    $(Xpath.concrete_checkbox).click(function (e) {
        var totalCount = $(Xpath.concrete_checkbox).length;
        var checkedCount = $(Xpath.concrete_checbox_checked).length;
        console.log(totalCount, checkedCount);

        var globalCheckbox = $(Xpath.global_checkbox);
        if (totalCount == checkedCount) {
            globalCheckbox.prop('indeterminate', false).prop('checked', true);
        } else if (checkedCount == 0) {
            globalCheckbox.prop('indeterminate', false).prop('checked', false);
        } else {
            globalCheckbox.prop('indeterminate', true).prop('checked', false);
        }
    });
});