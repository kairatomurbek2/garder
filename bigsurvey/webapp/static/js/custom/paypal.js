var selectors = {
    modal: '#pay-modal',
    tests: 'input[name="tests"]',
    payButton: '[data-action="pay"]',
    spinner: '[data-content="spinner"]',
    errorAlert: '[data-content="error-alert"]',
    errorMessage: '[data-content="error-message"]',
    step1: '[data-content="step-1"]',
    step2: '[data-content="step-2"]',
    creationLink: '[data-content="creation-link"]',
    approvalLink: '[data-content="approval-link"]',
    totalAmount: '[data-content="total-amount"]'
};

var hideElementWithDelay = function (element, delay, hidingDuration) {
    delay = delay || 5000;
    hidingDuration = hidingDuration || 'slow';
    setTimeout(function () {
        element.hide(hidingDuration);
    }, delay);
};

var getSelectedTests = function () {
    var selectedTests = [];
    $(selectors.tests).filter(':checked').each(function () {
        selectedTests.push($(this).val());
    });
    return selectedTests;
};

var resetModal = function () {
    $(selectors.step1).show().fadeTo('fast', 1);
    $(selectors.step2).fadeTo('fast', 1).hide();
    $(selectors.spinner).hide();
    $(selectors.errorAlert).hide();
    $(selectors.errorMessage).text('');
    $(selectors.approvalLink).removeAttr('href');
    $(selectors.totalAmount).text('');
};

var setPayButtonState = function () {
    if ($(selectors.tests).filter(':checked').size() > 0) {
        $(selectors.payButton).removeAttr('disabled');
    } else {
        $(selectors.payButton).attr('disabled', 'disabled');
    }
};

var createPayment = function (tests, successHandler) {
    $.ajax(Urls.test_pay_paypal, {
        method: 'post',
        data: {
            'tests': tests
        },
        traditional: true,
        success: successHandler
    });
};

var isPaymentProcessing = false;

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

    $(selectors.creationLink).click(function (e) {
        e.preventDefault();

        if (!isPaymentProcessing) {
            isPaymentProcessing = true;

            var selectedTests = getSelectedTests();

            $(selectors.step1).fadeTo('fast', 0.5);
            $(selectors.spinner).show();

            createPayment(selectedTests, function (response) {
                if (!isPaymentProcessing) {
                    resetModal();
                    return;
                }
                if (response.status == 'success') {
                    $(selectors.step1).hide();
                    $(selectors.errorAlert).hide();
                    $(selectors.step2).show();
                    $(selectors.totalAmount).text(response.total_amount);
                    $(selectors.approvalLink).attr('href', response.approval_url);
                } else if (response.status == 'error') {
                    $(selectors.step1).fadeTo('fast', 1);
                    $(selectors.errorAlert)
                        .show()
                        .find(selectors.errorMessage)
                        .text(response.message);
                    hideElementWithDelay($(selectors.errorAlert));
                }
                $(selectors.spinner).hide();
                isPaymentProcessing = false;
            });
        }

        return false;
    });

    $(selectors.approvalLink).click(function (e) {
        $(selectors.step2).fadeTo('fast', 0.5);
        $(selectors.spinner).show();
    });
});