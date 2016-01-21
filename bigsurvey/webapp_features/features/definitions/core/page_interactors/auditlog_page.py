from webapp_features.features.definitions.core.page_interactors import _helper


def assert_that_auditlog_records_are_shown(data):
    _helper.assert_row_exists_in_table(data)
