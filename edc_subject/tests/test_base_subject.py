from django.test import TestCase

from ..models import BaseSubject


class TestModel(BaseSubject):
    pass

    class Meta:
        app_label = 'edc_subject'


class BaseSubjectTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def tearDown(self):
        pass

    def test_insertdummy_id(self):
        """Test that the base subject inserts a dummy identifier"""
        test_model = TestModel(first_name='BELLA', last_name='BENE', gender='F')
        print (test_model.__dict__)
        self.assertIsNone(test_model.subject_identifier_as_pk, "Failed: Not None")
        self.assertIsNotNone(test_model.subject_identifier_as_pk, "Failed: None")
