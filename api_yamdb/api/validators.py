from datetime import datetime

from rest_framework import validators


def validate_year(value_year):
    if value_year > datetime.now().year:
        raise validators.ValidationError(
            'Год создания не может быть больше чем текущий!'
        )
    elif value_year < 0:
        raise validators.ValidationError(
            'Год создания не может быть отрицательным!'
        )
