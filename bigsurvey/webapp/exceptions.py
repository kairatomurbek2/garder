import json


class PaymentWasNotCreatedError(Exception):
    def __init__(self, errors):
        self.errors = errors
        self.message = json.dumps(self.errors, indent=4)

    def __str__(self):
        return self.message