from django.core.exceptions import ValidationError


def validate_blank_content(value):
    if value == "":
        raise ValidationError("Content cannot be blank!")
    return value
