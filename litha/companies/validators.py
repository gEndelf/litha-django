from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.files.images import get_image_dimensions


def stop_list_validator(value):
    stop_list = ['badname']
    if value in stop_list:
        raise ValidationError('Invalid name')


def validate_image_size(value):
    width, height = get_image_dimensions(value)
    if width > 300 or height > 300:
        raise ValidationError('Image is too big')


validate_phone = RegexValidator(r"^\+?[0-9]{3}-?[0-9]{6,12}$")
