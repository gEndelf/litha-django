import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView

from companies.models import Company
from companies.forms import CompanyForm, LogoUploadForm


class IndexView(TemplateView):

    template_name = "companies/index.html"


class CompanyFormView(TemplateView):

    template_name = "companies/company_form.html"

    def get_context_data(self, **kwargs):
        context = super(CompanyFormView, self).get_context_data(**kwargs)
        context['form'] = CompanyForm(scope_prefix='company')
        return context


class CompanyListView(View):

    def get(self, *args, **kwargs):
        companies = []
        for company in Company.objects.all():
            companies.append(company.serialize())
        return HttpResponse(json.dumps({'companies': companies}),
                            content_type="application/json")


class CompanyDetailView(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(CompanyDetailView, self).dispatch(*args, **kwargs)

    def get(self, *args, **kwargs):
        # Get company
        company = get_object_or_404(Company, pk=self.kwargs.get('pk'))
        return HttpResponse(json.dumps({'company': company.serialize()}),
                            content_type="application/json")

    def post(self, *args, **kwargs):
        # Upload logo
        company = get_object_or_404(Company, pk=self.kwargs.get('pk'))
        form = LogoUploadForm(self.request.POST,
                              self.request.FILES,
                              instance=company)
        if form.is_valid():
            company = form.save()
            data = {'url': company.logo.url}
        else:
            data = {'error': ', '.join(form.errors['logo'])}
        return HttpResponse(json.dumps(data),
                            content_type="application/json")

    def put(self, *args, **kwargs):
        # Update company
        company = get_object_or_404(Company, pk=self.kwargs.get('pk'))
        form = CompanyForm(data=json.loads(self.request.body), instance=company)
        if form.is_valid():
            company = form.save()
            data = {'company': company.serialize()}
        else:
            data = {'errors': form.errors}
        return HttpResponse(json.dumps(data),
                            content_type="application/json")
