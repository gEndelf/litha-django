from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator

from companies.validators import (
    stop_list_validator,
    validate_phone,
    validate_image_size)


class Company(models.Model):

    STATUSES = [
        ('active', 'ACTIVE'),
        ('blocked', 'BLOCKED'),
        ('deleted', 'DELETED'),
    ]

    name = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            MinLengthValidator(2),
            RegexValidator(r"^[a-zA-Z]+[a-zA-Z0-9_ ]?\w$"),
            stop_list_validator,
        ])
    description = models.CharField(max_length=350, blank=True)
    mobile = models.CharField(
        max_length=12,
        blank=True,
        validators=[validate_phone])
    phone1 = models.CharField(
        max_length=12,
        validators=[validate_phone])
    phone2 = models.CharField(
        max_length=12,
        blank=True,
        validators=[validate_phone])
    website = models.URLField(blank=True)
    address = models.TextField()
    logo = models.ImageField(
        upload_to='logos',
        blank=True,
        validators=[validate_image_size])
    status = models.CharField(
        max_length=10,
        choices=STATUSES,
        default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'companies'

    def serialize(self):
        result = {
            'id': self.pk,
            'name': self.name,
            'description': self.description,
            'mobile': self.mobile,
            'phone1': self.phone1,
            'phone2': self.phone2,
            'website': self.website,
            'address': self.address,
            'logo': self.logo.url if self.logo else '',
            'status': self.status,
            'created_at': self.created_at.strftime('%c'),
            'updated_at': self.updated_at.strftime('%c'),
        }
        return result
