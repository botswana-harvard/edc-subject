from uuid import uuid4

from edc_base.model.models import BaseUuidModel

from django.core.validators import RegexValidator
from django.db import models
from django_crypto_fields.fields import FirstnameField, LastnameField, EncryptedCharField

from edc_base.model.fields import IsDateEstimatedField
from edc_base.model.validators import dob_not_future, MinConsentAge, MaxConsentAge
from edc_constants.choices import GENDER_UNDETERMINED

from ..managers import BaseSubjectManager


class BaseSubject (BaseUuidModel):
    """Base for consent and registered subject models.

    .. note:: the field subject_identifier_as_pk is in both
              models but the values are independent; that
              is, consent.subject_identifier_as_pk !=
              registered_subject.subject_identifier_as_pk.
    """

    subject_identifier_as_pk = models.UUIDField(
        verbose_name="Subject Identifier as pk",
        default=uuid4
    )

    subject_identifier_aka = models.CharField(
        verbose_name="Subject Identifier a.k.a",
        max_length=50,
        null=True,
        editable=False,
        help_text='track a previously allocated identifier.'
    )

    dm_comment = models.CharField(
        verbose_name="Data Management comment",
        max_length=150,
        null=True,
        editable=False,
        help_text='see also edc.data manager.'
    )

    # may not be available when instance created (e.g. infants prior to birth report)
    first_name = FirstnameField(
        null=True,
    )

    # may not be available when instance created (e.g. infants or household subject before consent)
    last_name = LastnameField(
        verbose_name="Last name",
        null=True,
    )

    # may not be available when instance created (e.g. infants)
    initials = EncryptedCharField(
        validators=[RegexValidator(regex=r'^[A-Z]{2,3}$',
                                   message=('Ensure initials consist of letters '
                                            'only in upper case, no spaces.')), ],
        null=True,
    )

    dob = models.DateField(
        verbose_name="Date of birth",
        validators=[
            dob_not_future,
            MinConsentAge,
            MaxConsentAge,
        ],
        null=True,
        blank=False,
        help_text="Format is YYYY-MM-DD",
    )

    is_dob_estimated = IsDateEstimatedField(
        verbose_name="Is date of birth estimated?",
        null=True,
        blank=False,
    )

    gender = models.CharField(
        verbose_name="Gender",
        choices=GENDER_UNDETERMINED,
        max_length=1,
        null=True,
        blank=False,
    )

    subject_type = models.CharField(
        max_length=25,
    )

    objects = BaseSubjectManager()

    def natural_key(self):
        return (self.subject_identifier_as_pk, )

    class Meta:
        abstract = True
