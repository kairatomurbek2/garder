var AjaxForm = function (form, successHandler) {
    this.form = form;
    this.successHandler = successHandler;

    this.submit = function (event) {
        event.preventDefault();
        var url = this.form.attr('action');
        var method = this.form.attr('method');
        var data = new FormData(this.form);

        $.ajax(url, {
            method: method,
            data: data,
            contentType: false,
            processData: false,
            success: this.successHandler
        });
        return false;
    };

    form.submit(this.submit);
};