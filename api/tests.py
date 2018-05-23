# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import json
from api.models import Contact


class ModelTestCase(TestCase):
    """Test suite for contact model."""

    def setUp(self):
        """Setting up basic test requiments"""
        self.contact_email = "onsite.test@plivo.com"
        self.contact_name = "Onsite test"
        self.contact = Contact(name=self.contact_name,
                                  email=self.contact_email)

    def test_model_can_create_a_contact(self):
        """Testing if contact model can create an object"""
        old_count = Contact.objects.count()
        self.contact.save()
        new_count = Contact.objects.count()
        self.assertEqual(old_count+1, new_count)

    def test_model_cannot_create_a_contact_with_same_email(self):
        """Testing if contact model can create an object"""
        old_count = Contact.objects.count()
        self.contact.save()

        self.contact_email = "onsite.test@plivo.com"
        self.contact_name = "Onsite test1"
        with self.assertRaises(IntegrityError):
            self.contact1 = Contact(name=self.contact_name,
                                   email=self.contact_email)
            self.contact1.save()

    def test_model_can_read_a_contact(self):
        """Testing if contact model can read an object"""
        self.contact.save()
        contact = Contact.objects.get(email=self.contact_email)
        self.assertEqual(self.contact_email, contact.email)
        self.assertEqual(self.contact_name, contact.name)
    # TODO: Add model test for Update, Delete

    def test_model_can_update_a_contact(self):
        """ Test for updating a contact """
        pass

    def test_model_can_delete_a_contact(self):
        """ Test for deleting a contact """
        pass


class ViewTestCase(TestCase):
    """ Test suite for view level operations."""

    def _get_auth_token(self):
        return self.token

    def _generate_dummy_user(self):
        """ Generate dummy user and it's auth token. """
        test_user = User.objects.create_user('foo', password='bar')
        test_user.is_superuser = True
        test_user.is_admin = True
        test_user.save()
        token, created = Token.objects.get_or_create(user=test_user)
        self.token = token.key

    def setUp(self):
        """Setting up basic test requiments for view tests."""
        self.client = APIClient()
        self._generate_dummy_user()

        self.contact_data = {
            'name': 'Onsite test',
            'email': 'onsite.test@plivo.com',
            'token': self._get_auth_token()
        }


    def test_api_can_create_a_contact(self):
        """Test the api has contact creation capability."""

        self.response = self.client.post(
            reverse('create'),
            self.contact_data
        )
        response_data = json.loads(self.response.content)
        self.assertEqual(response_data['status'], 'success')

    def test_api_cannot_create_a_contact_with_same_email(self):
        """ Cannot create multiple contact with same email ids"""
        # Create one contact with below data
        self.client.post(
            reverse('create'),
            self.contact_data
        )

        # Create one contact with updated data but same email
        contact_data_with_same_email = {
            'name': 'Onsite test 2',
            'email': 'onsite.test@plivo.com',
            'token': self._get_auth_token()
        }
        response = self.client.post(
            reverse('create'),
            contact_data_with_same_email
        )
        response_data = json.loads(response.content)
        self.assertEqual(response_data['status'], 'failed')

    def test_api_can_read_a_contact(self):
        """ Read a contact """
        pass

    def test_api_can_update_a_contact(self):
        """ Test for updating a contact """
        pass

    def test_api_can_delete_a_contact(self):
        """ Test for deleting a contact """
        pass
    # TODO: Write tests for Read, Update, Delete

