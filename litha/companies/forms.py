from django.forms import ModelForm
from django.utils import timezone

from djangular.forms.angular_model import NgModelFormMixin
from djangular.forms import NgFormValidationMixin

from companies.models import Company


class CompanyForm(NgModelFormMixin, NgFormValidationMixin, ModelForm):

    form_name = "company_form"

    class Meta:
        model = Company
        exclude = [
            'logo',
            'created_at',
            'updated_at',
        ]

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            widget = self.fields[field_name].widget
            widget.attrs['server-error'] = 'server-error'
            if field_name == 'name':
                widget.attrs['ng-minlength'] = 2
                widget.attrs['ng-pattern'] = r"/^[a-zA-Z]+[a-zA-Z0-9_]?\w$/"
            elif field_name in ['mobile', 'phone1', 'phone2']:
                widget.attrs['ng-pattern'] = r"/^\+?[0-9]{3}-?[0-9]{6,12}$/"

    def save(self, commit=True):
        instance = super(CompanyForm, self).save(commit=False)
        instance.updated_at = timezone.now()
        if commit:
            instance.save()
        return instance


class LogoUploadForm(ModelForm):

    class Meta:
        model = Company
        fields = ['logo']
