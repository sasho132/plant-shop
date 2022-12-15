import string
from django.core.exceptions import ValidationError


def validate_alphabet_characters(value):
    for char in value.lower():
        if not char.isalpha():
            raise ValidationError('Only letters are allowed')
        elif char.isalpha() and char not in string.ascii_lowercase:
            raise ValidationError('You are not allowed to use non-English characters')
