$(document).ready(function () {
    $(selectors.modal).on('hide.uk.modal', function () {
        location.href = Urls.unpaid_test_list;
    });

    var modal = UIkit.modal(selectors.modal);
    modal.show();

    $(selectors.creationLink).click(getCreationLinkHandler(tests));

    $(selectors.approvalLink).click(defaultApprovalLinkHandler);
});
