from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.utils import timezone
from .managers import CustomUserManager


class Bundle(models.Model):
    name = models.CharField(max_length=255)
    duration = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Bundle'
        verbose_name_plural = 'Bundles'


class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'


class Company(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    bin = models.CharField(max_length=12, validators=[MinLengthValidator(12)])
    address = models.TextField()
    face = models.TextField()
    face_phone = models.CharField(max_length=12, validators=[MinLengthValidator(11)])
    favourites = models.ManyToManyField('Worker')
    requisites = models.FileField(upload_to='docs/companies/requisites/')
    license = models.FileField(upload_to='docs/companies/license/')
    gos_reg = models.FileField(upload_to='docs/companies/gos_reg/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)
    expired_date = models.DateField()
    type = models.CharField(max_length=55, choices=[('company', 'company'), ('worker', 'worker'), ('admin', 'admin')])
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.expired_date = timezone.now()
        super(CustomUser, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class EmailCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)

    def __str__(self):
        return str(self.email) + ' ' + str(self.code)

    class Meta:
        verbose_name = 'EmailCode'
        verbose_name_plural = 'EmailCodes'


class Feedback(models.Model):
    author = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    rating = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date) + ' ' + self.author.name

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'


class Reply(models.Model):
    author = models.ForeignKey('worker', on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    file = models.FileField('docs/replies/')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date) + ' ' + self.author.name

    class Meta:
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'


class Section(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'


class Subsection(models.Model):
    name = models.CharField(max_length=255)
    section = models.ForeignKey('Section', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Subsection'
        verbose_name_plural = 'Subsections'


class Tender(models.Model):
    author = models.ForeignKey('Company', on_delete=models.CASCADE)
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    types_of_work = models.ManyToManyField('Subsection')
    date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField(null=True, blank=True)
    budget = models.FloatField()
    description = models.TextField(null=True, blank=True)
    docs = models.ManyToManyField('TenderDoc')
    is_active = models.BooleanField(default=True)
    replies = models.ManyToManyField('Reply')

    def __str__(self):
        return str(self.date) + ' ' + self.author.name

    class Meta:
        verbose_name = 'Tender'
        verbose_name_plural = 'Tenders'


class TenderDoc(models.Model):
    doc = models.FileField(upload_to='docs/tenders/')
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'TenderDoc'
        verbose_name_plural = 'TenderDocs'


class Worker(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    bin = models.CharField(max_length=12, validators=[MinLengthValidator(12)])
    description = models.TextField()
    director = models.TextField()
    phone = models.CharField(max_length=12, validators=[MinLengthValidator(11)])
    rating = models.FloatField()
    feedbacks = models.ManyToManyField('feedback')
    cities = models.ManyToManyField('city')
    types_of_work = models.ManyToManyField('subsection')
    docs = models.ManyToManyField('WorkerDoc')

    def __str__(self):
        return str(self.name) + ' ' + str(self.bin)

    class Meta:
        verbose_name = 'Worker'
        verbose_name_plural = 'Workers'


class WorkerDoc(models.Model):
    doc = models.FileField(upload_to='docs/workers/')
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'WorkerDoc'
        verbose_name_plural = 'WorkerDocs'
