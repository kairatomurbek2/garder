selectors.payButton = '[data-action="pay"]';

var getSelectedTests = function () {
    var selectedTests = [];
    $(selectors.tests).filter(':checked').each(function () {
        selectedTests.push($(this).val());
    });
    return selectedTests;
};

var setPayButtonState = function () {
    if ($(selectors.tests).filter(':checked').size() > 0) {
        $(selectors.payButton).removeAttr('disabled');
    } else {
        $(selectors.payButton).attr('disabled', 'disabled');
    }
};

$(document).ready(function () {
    setPayButtonState();
    $(selectors.tests).click(setPayButtonState);

    $(selectors.modal).on('hide.uk.modal', function () {
        isPaymentProcessing = false;
        resetModal();
    });

    $(selectors.payButton).click(function () {
        var selectedTests = getSelectedTests();
        if (!$.isEmptyObject(selectedTests)) {
            var modal = UIkit.modal(selectors.modal);
            modal.show();
        }
    });

    $(selectors.creationLink).click(getCreationLinkHandler(getSelectedTests));

    $(selectors.approvalLink).click(defaultApprovalLinkHandler);
});