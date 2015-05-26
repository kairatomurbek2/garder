var selectors = {
    pay_button: '[data-action="pay"]',
    payment_creation_link: 'a[data-content="paypal-payment-creation-link"]',
    errors: '[data-content="errors"]',
    error_message: '[data-content="error-message"]',
    step_1: '[data-content="step-1"]',
    step_2: '[data-content="step-2"]',
    paypal_approval_link: 'a[data-content="paypal-approval-link"]',
    credit_card_form: 'form[name="credit-card-form"]',
    credit_card_form_container: '[data-content="credit-card-form"]',
    credit_card_form_wrapper: '[data-content="credit-card-form-wrapper"]',
    spinner_paypal: '[data-content="spinner-paypal"]',
    spinner_credit_card: '[data-content="spinner-credit-card"]'
};

$(document).ready(function () {
    $(selectors.errors).off('click', '.uk-close', function (e) {
        $(this).parent().hide();
    });

    $(selectors.pay_button).click(function () {
        var test_pk = $(this).data('test-pk');
        var actual_paypal_url = paypal_url.replace(0, test_pk);
        var actual_credit_card_url = credit_card_url.replace(0, test_pk);
        $(selectors.payment_creation_link).attr('href', actual_paypal_url);
        $(selectors.credit_card_form).attr('action', actual_credit_card_url);
    });

    $(selectors.credit_card_form_container).on('submit', selectors.credit_card_form, function (e) {
        e.preventDefault();

        $(selectors.credit_card_form_wrapper).fadeTo('fast', 0.5);
        $(selectors.spinner_credit_card).show();

        var url = $(this).attr('action');
        var method = $(this).attr('method');

        $.ajax(url, {
            method: method,
            data: new FormData(this),
            processData: false,
            contentType: false,
            success: function (response) {
                $(selectors.spinner_credit_card).hide();
                $(selectors.credit_card_form_wrapper).fadeTo('fast', 1);
                $(selectors.credit_card_form_container).html(response);
                $(selectors.credit_card_form).attr('action', url);
            }
        });

        return false;
    });

    $(selectors.payment_creation_link).click(function (e) {
        e.preventDefault();

        var url = $(this).attr('href');

        $(selectors.step_1).fadeTo('fast', 0.5);
        $(selectors.spinner_paypal).show();

        $.ajax(url, {
            method: 'post',
            success: function (response) {
                if (response.status == 'success') {
                    $(selectors.step_1).hide();
                    $(selectors.errors).hide();
                    $(selectors.step_2).show();
                    $(selectors.paypal_approval_link).attr('href', response.approval_url);
                } else if (response.status == 'error') {
                    $(selectors.step_1).fadeTo('fast', 1);
                    $(selectors.errors)
                        .show()
                        .find(selectors.error_message)
                        .text(response.message);
                }
                $(selectors.spinner_paypal).hide();
            }
        });

        return false;
    });

    $(selectors.paypal_approval_link).click(function (e) {
        $(selectors.step_2).fadeTo('fast', 0.5);
        $(selectors.spinner_paypal).show();
    });
});