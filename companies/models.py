from django.db import models
from django.utils.text import slugify
from django_countries.fields import CountryField
from services.choices import status
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from services.mixin import DateMixin


def upload_profile_photo(instance, filename):
    return f"companies/{slugify(instance.email)}/{filename}"


def upload_background_image(instance, filename):
    return f"companies/background/{slugify(instance.email)}/{filename}"


class Company(DateMixin):
    name = models.CharField(max_length=100)
    profile_photo = models.ImageField(upload_to=upload_profile_photo, blank=True, null=True)
    background_image = models.ImageField(upload_to=upload_background_image, blank=True, null=True)
    country = CountryField()


class WorkerLevel(MPTTModel):
    level = models.CharField(max_length=30)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="children")

    def __str__(self):
        return self.level


class JobDetail(DateMixin):
    status = models.CharField(choices=status, max_length=20)

    # profile_photo = models.ImageField(upload_to=upload_profile_photo, blank=True, null=True)   BU FIELD COMPANY MODELINNEN GELECEK
    # background_image = models.ImageField(upload_to=upload_background_image, blank=True, null=True)

    title = models.CharField(max_length=50)

    # company_name = models.CharField(max_length=50) BU FIELD COMPANY MODELINNEN GELECEK

    # location = CountryField() BU FIELD COMPANY MODELINNEN GELECEK
    experience = models.CharField(max_length=40)
    worker_level = models.ForeignKey(WorkerLevel, on_delete=models.SET_NULL, blank=True, null=True)
    employee_type = models.ForeignKey("profiles.EmploymentType", on_delete=models.SET_NULL, blank=True, null=True)
    offer_salary = models.PositiveIntegerField()
    job_description = models.CharField(max_length=250)
    requirements = RichTextField()
