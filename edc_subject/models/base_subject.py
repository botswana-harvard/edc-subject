from uuid import uuid4

from edc_base.model.models import BaseUuidModel

from django.core.validators import RegexValidator
from django.db import models
from django_crypto_fields.fields import FirstnameField, LastnameField, EncryptedCharField

from edc_base.model.fields import IsDateEstimatedField
from edc_base.model.validators import dob_not_future, MinConsentAge, MaxConsentAge
from edc_constants.choices import GENDER_UNDETERMINED

from ..exceptions import SubjectError
from ..managers import BaseSubjectManager


class BaseSubject (BaseUuidModel):
    """Base for consent and registered subject models.

    .. note:: the field subject_identifier_as_pk is in both
              models but the values are independent; that
              is, consent.subject_identifier_as_pk !=
              registered_subject.subject_identifier_as_pk.
    """

    # a signal changes subject identifier which messes up bhp_sync
    # this field is always available and is unique
    subject_identifier_as_pk = models.CharField(
        verbose_name="Subject Identifier as pk",
        max_length=50,
        null=True,
        db_index=True,
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
        null=True,
    )

    objects = BaseSubjectManager()

    def natural_key(self):
        return (self.subject_identifier_as_pk, )

    def insert_dummy_identifier(self):
        """Inserts a random uuid as a dummy identifier for a new instance.

        Model uses subject_identifier_as_pk as a natural key for
        serialization/deserialization. Value must not change once set."""

        # set to uuid if new and not specified
        if not self.id or not self.subject_identifier_as_pk:
            subject_identifier_as_pk = str(uuid4())
            self.subject_identifier_as_pk = subject_identifier_as_pk  # this will never change
        # never allow subject_identifier_as_pk as None
        if not self.subject_identifier_as_pk:
            raise SubjectError('Attribute subject_identifier_as_pk on model '
                               '{0} may not be left blank. Expected to be set '
                               'to a uuid already.'.format(self._meta.object_name))

    def get_subject_type(self):
        """Returns a subject type.
        Usually overridden.

        ..note:: this is important for the link between
                 dashboard and membership form category."""

        return self.subject_type

    def save(self, *args, **kwargs):
        self.subject_type = self.get_subject_type()
        self.insert_dummy_identifier()
        super(BaseSubject, self).save(*args, **kwargs)

    class Meta:
        abstract = True
