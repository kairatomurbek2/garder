from webapp import models


class InvalidVendor(Exception):
    def __init__(self, vendor, available_vendors, *args, **kwargs):
        self.vendor = vendor
        self.available_vendors = available_vendors

    def __str__(self):
        return 'Invalid vendor: %s. Available vendors: %s.' % (self.vendor, ', '.join(self.available_vendors))


class RawSqlQuery(object):
    available_vendors = ['mysql', 'sqlite', 'postgresql', 'oracle']

    @classmethod
    def get_query(cls, vendor):
        if vendor not in cls.available_vendors:
            raise InvalidVendor(vendor, cls.available_vendors)
        return getattr(cls, 'as_%s' % vendor)()

    @classmethod
    def as_sql(cls):
        raise NotImplementedError

    @classmethod
    def as_mysql(cls):
        return cls.as_sql()

    @classmethod
    def as_sqlite(cls):
        return cls.as_sql()

    @classmethod
    def as_postgresql(cls):
        return cls.as_sql()

    @classmethod
    def as_oracle(cls):
        return cls.as_sql()


class HazardPriorityQuery(RawSqlQuery):
    @classmethod
    def as_mysql(cls):
        return '''
        SELECT
            CASE WHEN (SELECT install_date from webapp_bpdevice WHERE id = webapp_hazard.bp_device_id) IS NULL THEN
                CASE WHEN (SELECT due_test_date from webapp_bpdevice WHERE id = webapp_hazard.bp_device_id) IS NULL THEN
                    1000000
                ELSE
                    DATEDIFF((SELECT due_test_date from webapp_bpdevice WHERE id = webapp_hazard.bp_device_id), CURRENT_TIMESTAMP)
                END
            ELSE
                100000 + DATEDIFF(CURRENT_TIMESTAMP, (SELECT install_date from webapp_bpdevice WHERE id = webapp_hazard.bp_device_id))
            END
        '''

    @classmethod
    def as_sqlite(cls):
        return '''
        SELECT
            CASE WHEN (SELECT install_date from webapp_bpdevice WHERE id = webapp_hazard.bp_device_id) IS NULL THEN
                CASE WHEN (SELECT due_test_date from webapp_bpdevice WHERE id = webapp_hazard.bp_device_id) IS NULL THEN
                    1000000
                ELSE
                    cast(round(julianday((SELECT due_test_date from webapp_bpdevice WHERE id = webapp_hazard.bp_device_id)) - julianday() + 0.5) as int)
                END
            ELSE
                100000 + cast(round(julianday() - julianday((SELECT install_date from webapp_bpdevice WHERE id = webapp_hazard.bp_device_id)) - 0.5) as int)
            END
        '''


class SetLastSurveyDateQuery(RawSqlQuery):
    sites_table_name = models.Site._meta.db_table
    surveys_table_name = models.Survey._meta.db_table

    @classmethod
    def as_sql(cls):
        query = '''
        UPDATE %(sites_table_name)s
            SET last_survey_date =
                (SELECT MAX(%(surveys_table_name)s.survey_date)
                    FROM %(surveys_table_name)s
                    WHERE %(surveys_table_name)s.site_id = %(sites_table_name)s.id)
        '''
        return query % {'sites_table_name': cls.sites_table_name, 'surveys_table_name': cls.surveys_table_name}


class SetDueInstallTestDateQuery(RawSqlQuery):
    sites_table_name = models.Site._meta.db_table
    hazards_table_name = models.Hazard._meta.db_table
    bp_devices_table_name = models.BPDevice._meta.db_table

    @classmethod
    def as_sql(cls):
        query = '''
        UPDATE %(sites_table_name)s
            SET %(sites_table_name)s.due_install_test_date =
                (SELECT MIN(%(bp_devices_table_name)s.due_test_date)
                    FROM %(bp_devices_table_name)s
                    WHERE %(bp_devices_table_name)s.id IN (SELECT %(hazards_table_name)s.bp_device_id
                        FROM %(hazards_table_name)s
                        WHERE %(hazards_table_name)s.site_id = %(sites_table_name)s.id))
        '''
        return query % {
            'sites_table_name': cls.sites_table_name,
            'hazards_table_name': cls.hazards_table_name,
            'bp_devices_table_name': cls.bp_devices_table_name
        }


class ResetAutoincrementFieldsForTesting(RawSqlQuery):

    @classmethod
    def as_sqlite(cls):
        return "delete from sqlite_sequence;"
