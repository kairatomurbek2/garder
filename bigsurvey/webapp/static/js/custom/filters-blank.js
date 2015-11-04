function setup_blank_checks(){
    var blank_fields = [
        'street_number',
        'address2',
        'apt',
        'zip',
        'cust_address_1',
        'cust_address_2',
        'cust_apt',
        'cust_city',
        'cust_zip',
        'route',
        'meter_number',
        'meter_size',
        'meter_reading',
        'connect_date'
    ];
    var blank_checkbox_id, blank_field_id;
    for(var index in blank_fields) {
        if (blank_fields.hasOwnProperty(index)) {
            blank_field = blank_fields[index];
            blank_field_id = "#id_" + blank_field;
            blank_checkbox_id = "#id_" + blank_field + "_blank";
            (function (bfid, bcid) {
                $(bcid).click(function () {
                    if (this.checked) {
                        $(bfid).val('');
                        $(bfid).prop('disabled', true);
                    }
                    else {
                        $(bfid).prop('disabled', false);
                    }
                });
            })(blank_field_id, blank_checkbox_id);
        }
    }
}
