from django.db import models
from datetime import date, datetime
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Propstatus(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'ad status'
        verbose_name_plural = 'ad statuses'

class Application(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name= _('applicant'), related_name='applicant')
    description = models.TextField(max_length=1500, blank=True, verbose_name= _('description'),)
    created = models.DateTimeField(default=timezone.now, blank=True, verbose_name= _('created'),)
    approvals = models.ManyToManyField('Proposal', blank=True, related_name=_('approvals'),)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'application'
        verbose_name_plural = 'applications'

class ProposalQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(adstatus_id = '2').order_by('-created')

class ProposalManager(models.Manager):
    def get_queryset(self):
        return ProposalQuerySet(self.model, using=self._db)

    def all_active(self):
        return self.get_queryset().active()

class Proposal(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name= _('created'), related_name='author')
    user_contact = models.CharField(max_length=150, verbose_name = _('contacts'),)
    title = models.CharField(max_length=100, verbose_name= _('title'),)
    city = models.CharField(max_length=20, verbose_name= _('city'),)
    amount = models.IntegerField(verbose_name= _('amount'),)
    applicants_number = models.IntegerField(default='1', verbose_name= _('applicants number'),)
    description = models.TextField(max_length=1500, blank=True, verbose_name= _('description'),)
    created = models.DateTimeField(default=timezone.now, blank=True, verbose_name= _('created'),)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name= _('updated'),)
    is_featured = models.BooleanField(default=False)
    adstatus_id = models.ForeignKey(Propstatus, on_delete=models.DO_NOTHING, default='1')
    requests = models.ManyToManyField(Application, blank=True, related_name=_('requests'),)

    objects = ProposalManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'proposal'
        verbose_name_plural = 'proposals'
