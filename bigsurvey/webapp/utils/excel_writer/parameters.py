SITE_FIELDS = [
    ("pk", "ID"),
    ("pws", "PWS"),
    ("cust_number", "Account Number"),
    ("cust_code", "Customer Code"),
    ("cust_name", "Customer Name"),
    ("cust_address1", "Customer Address 1"),
    ("cust_address2", "Customer Address 2"),
    ("cust_apt", "Customer Apt."),
    ("cust_city", "Customer City"),
    ("cust_state", "Customer State"),
    ("cust_zip", "Customer ZIP"),
    ("street_number", "Service Street Number"),
    ("address1", "Service Address 1"),
    ("address2", "Service Address 2"),
    ("apt", "Service Apt."),
    ("city", "Service City"),
    ("state", "Service State"),
    ("zip", "Service ZIP"),
    ("potable_present",  "Potable Present"),
    ("fire_present", "Fire Present"),
    ("irrigation_present", "Irrigation Present"),
    ("status", "Site Status"),
    ("connect_date", "Connect Date"),
    ("last_survey_date", "Last Survey Date"),
    ("next_survey_date", "Next Survey Date"),
    ("due_install_test_date", "Due Install/Test Date"),
    ("route", "Seq. Route"),
    ("site_use", "Site Use"),
    ("site_type", "Site Type"),
    ("floors", "Floors Count"),
    ("interconnection_point", "Interconnection Point"),
    ("meter_number", "Meter Number"),
    ("meter_size", "Meter Size"),
    ("meter_reading", "Meter Reading"),
    ("is_due_install", "Is Due Install"),
    ("is_backflow", "Is Backflow"),
    ("contact_phone", "Contact Phone"),
    ("contact_fax", "Contact FAX"),
    ("contact_email", "Contact Email"),
    ("notes", "Notes"),
]

HAZARD_FIELDS = [
    ("service_type", "Service Type"),
    ("hazard_type", "Hazard Type"),
    ("location1", "Location 1"),
    ("location2", "Location 2"),
    ("bp_type_required", "Assembly Type Required"),
    ("regulation_type", "Regulation"),
    ("assembly_status", "Assembly Status"),
    ("pump_present", "Pump Present"),
    ("additives_present", "Additives Present"),
    ("cc_present", "CC Present"),
    ("aux_water", "Auxiliary Water"),
    ("hazard_degree", "Hazard Degree"),
    ("latitude", "Latitude"),
    ("longitude", "Longitude"),
    ("is_present", "Is Present"),
    ("notes", "Notes"),
]

BP_DEVICE_FIELDS = [
    ("assembly_location", "Assembly Location"),
    ("installed_properly", "Installed Properly"),
    ("installer", "Installer"),
    ("install_date", "Install Date"),
    ("replace_date", "Replace Date"),
    ("orientation", "Orientation"),
    ("bp_type_present", "Assembly Type Present"),
    ("bp_size", "BP Size"),
    ("manufacturer", "BP Manufacturer"),
    ("model_no", "BP Model No."),
    ("serial_no", "BP Serial No."),
    ("due_test_date", "Due Test Date"),
    ("notes", "Notes"),
]

BOOLEAN_FIELDS = [
    "potable_present",
    "fire_present",
    "irrigation_present",
    "is_due_install",
    "is_backflow",
    "pump_present",
    "additives_present",
    "cc_present",
    "aux_water",
    "is_present",
    "installed_properly",
]

DATE_FIELDS = [
    "connect_date",
    "next_survey_date",
    "last_survey_date",
    "due_install_test_date",
    "install_date",
    "replace_date",
    "due_install_date",
    "due_test_date",
]