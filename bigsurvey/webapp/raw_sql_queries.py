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
            CASE WHEN install_date IS NULL THEN
                CASE WHEN due_test_date IS NULL THEN
                    1000000
                ELSE
                    DATEDIFF(due_test_date, CURRENT_TIMESTAMP)
                END
            ELSE
                100000 + DATEDIFF(CURRENT_TIMESTAMP, install_date)
            END
        '''

    @classmethod
    def as_sqlite(cls):
        return '''
        SELECT
            CASE WHEN install_date IS NULL THEN
                CASE WHEN due_test_date IS NULL THEN
                    1000000
                ELSE
                    cast(round(julianday(due_test_date) - julianday() + 0.5) as int)
                END
            ELSE
                100000 + cast(round(julianday() - julianday(install_date) - 0.5) as int)
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

    @classmethod
    def as_sql(cls):
        query = '''
        UPDATE %(sites_table_name)s
            SET due_install_test_date =
                (SELECT MIN(%(hazards_table_name)s.due_test_date)
                    FROM %(hazards_table_name)s
                    WHERE %(hazards_table_name)s.site_id = %(sites_table_name)s.id)
        '''
        return query % {'sites_table_name': cls.sites_table_name, 'hazards_table_name': cls.hazards_table_name}


class ResetAutoincrementFieldsForTesting(RawSqlQuery):

    @classmethod
    def as_sqlite(cls):
        return "delete from sqlite_sequence;"
