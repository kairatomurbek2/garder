var selectors = {
    payButton: '[data-action="pay"]',
    spinner: '[data-content="spinner"]',
    errorAlert: '[data-content="error-alert"]',
    errorMessage: '[data-content="error-message"]',
    step1: '[data-content="step-1"]',
    step2: '[data-content="step-2"]',
    creationLink: '[data-content="creation-link"]',
    approvalLink: '[data-content="approval-link"]'
};

var hideElementWithDelay = function (element, delay, hidingDuration) {
    delay = delay || 5000;
    hidingDuration = hidingDuration || 'slow';
    setTimeout(function () {
        element.hide(hidingDuration);
    }, delay);
};

$(document).ready(function () {
    $(selectors.payButton).click(function () {
        var paypalUrl = $(this).data('paypal-url');
        $(selectors.creationLink).attr('href', paypalUrl);
    });

    $(selectors.creationLink).click(function (e) {
        e.preventDefault();

        var url = $(this).attr('href');

        $(selectors.step1).fadeTo('fast', 0.5);
        $(selectors.creationLink).removeAttr('href');
        $(selectors.spinner).show();

        $.ajax(url, {
            method: 'post',
            success: function (response) {
                if (response.status == 'success') {
                    $(selectors.step1).hide();
                    $(selectors.errorAlert).hide();
                    $(selectors.step2).show();
                    $(selectors.approvalLink).attr('href', response.approval_url);
                } else if (response.status == 'error') {
                    $(selectors.step1).fadeTo('fast', 1);
                    $(selectors.errorAlert)
                        .show()
                        .find(selectors.errorMessage)
                        .text(response.message);
                    hideElementWithDelay($(selectors.errorAlert));
                    $(selectors.creationLink).attr('href', url);
                }
                $(selectors.spinner).hide();
            }
        });

        return false;
    });

    $(selectors.approvalLink).click(function (e) {
        $(selectors.step2).fadeTo('fast', 0.5);
        $(selectors.spinner).show();
    });
});