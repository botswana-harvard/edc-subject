from django.db import connection

from django.test import TestCase

from ..models import BaseSubject


class TestModel(BaseSubject):
    pass

    class Meta:
        app_label = 'edc_subject'


class BaseSubjectTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        connection.cursor().execute(
            "DROP TABLE edc_subject_testmodel"
        )
        connection.cursor().execute(
            "CREATE TABLE edc_subject_testmodel ("
            "id varchar(100),"
            "created varchar(100),"
            "modified varchar(100),"
            "user_created varchar(50),"
            "user_modified varchar(50),"
            "hostname_created varchar(50),"
            "hostname_modified varchar(50),"
            "subject_identifier_as_pk varchar(50),"
            "subject_identifier_aka varchar(50),"
            "first_name varchar(100),"
            "last_name varchar(100),"
            "initials varchar(10),"
            "dm_comment varchar(255),"
            "dob varchar(25),"
            "is_dob_estimated varchar(100),"
            "gender varchar(1),"
            "subject_type varchar(25),"
            "revision varchar(200)"
            ")"
        )

    def tearDown(self):
        connection.cursor().execute(
            "DROP TABLE edc_subject_testmodel"
        )

    def test_insertdummy_id(self):
        """Test that the base subject inserts a dummy identifier"""
        test_model = TestModel(first_name='BELLA', last_name='BENE', gender='F')
        self.assertIsNone(test_model.subject_identifier_as_pk, "Failed: Not None")
        test_model.save()
        self.assertIsNotNone(test_model.subject_identifier_as_pk, "Failed: None")
