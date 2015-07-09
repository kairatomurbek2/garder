from abc import ABCMeta, abstractmethod
from datetime import datetime
from django.db import IntegrityError
from django.db.models import NOT_PROVIDED
from main.parameters import Messages
from webapp import models
from webapp.utils.excel_parser import FOREIGN_KEY_FIELDS, CUST_NUMBER_FIELD_NAME, DATE_FIELDS, DateFormatError


class ValueCheckerFactory(object):
    @classmethod
    def get_checker(cls, field_name, **kwargs):
        model_field = models.Site._meta.get_field(field_name)
        required = not model_field.null and model_field.default == NOT_PROVIDED
        if cls._is_customer_number_field(field_name):
            builder = CustomerNumberValueCheckerBuilder()
        elif cls._is_foreign_key_field(field_name):
            model = model_field.rel.to
            builder = ForeignKeyValueCheckerBuilder()
            builder.set_required(required)
            builder.set_model(model)
        elif cls._is_date_field(field_name):
            date_format = kwargs.pop('date_format')
            builder = DateValueCheckerBuilder()
            builder.set_required(required)
            builder.set_date_format(date_format)
        else:
            builder = RequiredValueCheckerBuilder()
            builder.set_required(required)
        return builder.build()

    @classmethod
    def _is_customer_number_field(cls, field_name):
        return field_name == CUST_NUMBER_FIELD_NAME

    @classmethod
    def _is_foreign_key_field(cls, field_name):
        return field_name in FOREIGN_KEY_FIELDS

    @classmethod
    def _is_date_field(cls, field_name):
        return field_name in DATE_FIELDS


class ValueCheckerBuilder(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def build(self):
        pass


class RequiredValueCheckerBuilder(ValueCheckerBuilder):
    _required = True

    def set_required(self, required):
        self._required = required
        return self

    def build(self):
        required_value_checker = RequiredValueChecker()
        required_value_checker.required = self._required
        return required_value_checker


class CustomerNumberValueCheckerBuilder(RequiredValueCheckerBuilder):
    def build(self):
        # Customer Number always required
        self.set_required(True)
        customer_number_value_checker = CustomerNumberValueChecker()
        customer_number_value_checker.required = self._required
        return customer_number_value_checker


class ForeignKeyValueCheckerBuilder(RequiredValueCheckerBuilder):
    _model = None

    def set_model(self, model):
        self._model = model
        return self

    def build(self):
        foreign_key_value_checker = ForeignKeyValueChecker()
        foreign_key_value_checker.model = self._model
        foreign_key_value_checker.required = self._required
        return foreign_key_value_checker


class DateValueCheckerBuilder(RequiredValueCheckerBuilder):
    _date_format = None

    def set_date_format(self, date_format):
        self._date_format = date_format
        return self

    def build(self):
        date_value_checker = DateValueChecker()
        date_value_checker.date_format = self._date_format
        date_value_checker.required = self._required
        return date_value_checker


class ValueChecker(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def check(self, value, coords):
        pass


class RequiredValueChecker(ValueChecker):
    required = True

    def check(self, value, coords):
        if self.required and not value:
            raise IntegrityError(Messages.Import.required_value_is_empty % coords)


class CustomerNumberValueChecker(RequiredValueChecker):
    def __init__(self):
        self._customer_numbers = {}

    def check(self, value, coords):
        super(CustomerNumberValueChecker, self).check(value, coords)
        if value in self._customer_numbers:
            raise IntegrityError(Messages.Import.duplicate_cust_numbers % (self._customer_numbers[value], coords))
        self._customer_numbers[value] = coords


class ForeignKeyValueChecker(RequiredValueChecker):
    model = None
    available_values = None

    def get_available_values(self):
        if self.available_values is None:
            self.available_values = self.model.objects.values_list('pk', flat=True).order_by('pk')
        return self.available_values

    def check(self, value, coords):
        super(ForeignKeyValueChecker, self).check(value, coords)
        if value and value not in self.get_available_values():
            raise IntegrityError(Messages.Import.foreign_key_error % (coords, ', '.join(map(str, self.get_available_values())), value))


class DateValueChecker(RequiredValueChecker):
    date_format = None

    def check(self, value, coords):
        super(DateValueChecker, self).check(value, coords)
        if value:
            try:
                datetime.strptime(str(value), self.date_format)
            except ValueError:
                raise DateFormatError(Messages.Import.incorrect_date_format % (coords, self.date_format))