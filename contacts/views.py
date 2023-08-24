import json

from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from .exceptions import ContactNotFound
from .models import Contact
from .repositories.contacts_repo import ContactsRepository
from .serializers import ContactSerializer, MetaPagesSerializer
from django.core.paginator import Paginator
from drf_yasg import openapi


@swagger_auto_schema(
    tags=['contacts'],
    method='GET',
    manual_parameters=[
        openapi.Parameter(
            'page',
            openapi.IN_QUERY,
            description='Номер страницы',
            type=openapi.TYPE_INTEGER,
            required=False,
        ),
        openapi.Parameter(
            'per_page',
            openapi.IN_QUERY,
            description='Количество записей на странице',
            type=openapi.TYPE_INTEGER,
            required=False,
        ),
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description='Имя или номер телефона, по которому искать',
            type=openapi.TYPE_STRING,
            required=False,
        )
    ],
    responses={
        status.HTTP_200_OK: ContactSerializer(),
    }
)
@api_view(http_method_names=['GET'])
def get_contacts_view(request):
    """
    Список всех контактов

    Возможные параметры для передачи:
      - per_page - количество отображаемых объектов на странице
      - page - номер страницы
      - search - имя или номер телефона, по которому происходит поиск контактов
    """

    page_number = request.GET.get("page", 1)
    per_page = int(request.GET.get("per_page", 10))
    search = request.GET.get("search")
    relevant_contacts = ContactsRepository.find_relevant_contacts_by_phone_or_name(search)
    if not relevant_contacts:
        raise ContactNotFound
    paginator = Paginator(relevant_contacts, per_page)
    page_obj = paginator.get_page(page_number)
    meta_dict = {
        'page': page_obj.number,
        'page_size': paginator.per_page,
        'total': paginator.count,
        'page_count': paginator.num_pages
    }
    data = {
        'contacts': ContactSerializer(page_obj.object_list, many=True).data,
        'meta': MetaPagesSerializer(meta_dict).data
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
