import re

from typing import List
from contacts.models import Contact
from django.db.models import Q


class ContactsRepository:
    """Репозиторий для работы с Contacts"""

    @classmethod
    def is_phone_number(cls, input_string: str) -> bool:
        phone_pattern = re.compile(r'7(\s*\d{3}\s*\d{3}\s*\d{2}\s*\d{2})\b')
        return bool(phone_pattern.match(input_string))

    @classmethod
    def find_relevant_contacts_by_phone_or_name(
            cls,
            search: str | None
    ) -> List[Contact] | None:
        """Поиск контактов по номеру телефона, имени/имени и фамилии"""
        if not search:
            return list(Contact.objects.all())
        search = search.strip()
        if cls.is_phone_number(search):
            return list(Contact.objects.filter(phone__contains=search))

        search_words = search.strip().split()
        if len(search_words) == 2:
            first_name, last_name = search_words
            query = Q(first_name__icontains=first_name) & Q(last_name__icontains=last_name)
        else:
            query = Q()
            for word in search_words:
                query |= Q(first_name__icontains=word) | Q(last_name__icontains=word)

        return list(Contact.objects.filter(query))
