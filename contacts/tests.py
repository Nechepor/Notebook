from django.test import TestCase

from contacts.models import Contact
from contacts.repositories.contacts_repo import ContactsRepository
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from contacts.serializers import ContactSerializer


class ContactsRepositoryTestCase(TestCase):
    def setUp(self):
        # Создаем тестовые контакты
        Contact.objects.create(first_name="John", last_name="Doe", phone="+79999999999")
        Contact.objects.create(first_name="Jane", last_name="Doe", phone="+78888888888")
        Contact.objects.create(first_name="Alice", last_name="Smith", phone="+77777777777")

    def test_is_phone_number_valid(self):
        self.assertTrue(ContactsRepository.is_phone_number("79999999999"))
        self.assertTrue(ContactsRepository.is_phone_number("78888888888"))

    def test_is_phone_number_invalid(self):
        self.assertFalse(ContactsRepository.is_phone_number("invalid"))
        self.assertFalse(ContactsRepository.is_phone_number("8888888888"))

    def test_find_relevant_contacts_by_phone(self):
        contacts = ContactsRepository.find_relevant_contacts_by_phone_or_name("79999999999")
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0].first_name, "John")

    def test_find_relevant_contacts_by_name(self):
        contacts = ContactsRepository.find_relevant_contacts_by_phone_or_name("John")
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0].last_name, "Doe")

    def test_find_relevant_contacts_by_partial_name(self):
        contacts = ContactsRepository.find_relevant_contacts_by_phone_or_name("Doe")
        self.assertEqual(len(contacts), 2)

    def test_find_relevant_contacts_by_multiple_words(self):
        contacts = ContactsRepository.find_relevant_contacts_by_phone_or_name("John Doe")
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0].phone, "+79999999999")


class GetContactsViewTestCase(APITestCase):
    def setUp(self):
        Contact.objects.create(first_name="John", last_name="Doe", phone="79999999999")
        Contact.objects.create(first_name="Jane", last_name="Doe", phone="78888888888")

    def test_get_contacts_success(self):
        url = reverse("contact-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['contacts']), 2)  # Проверяем, что получили 2 контакта

    def test_get_contacts_with_search(self):
        url = reverse("contact-list")
        response = self.client.get(url, {'search': 'John'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['contacts']), 1)  # Проверяем, что получили 1 контакт

    def test_get_contacts_with_invalid_search(self):
        url = reverse("contact-list")
        response = self.client.get(url, {'search': 'NonExistent'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ContactCreateViewTestCase(APITestCase):
    def test_create_contact(self):
        url = reverse("contact-create")
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+79999999999",
            "email": "john@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_contact = Contact.objects.get(phone=response.json()["phone"])
        serializer = ContactSerializer(instance=created_contact)
        self.assertEqual(response.json(), serializer.data)
