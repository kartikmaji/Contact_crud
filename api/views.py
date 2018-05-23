# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError

from contact_book.model_ops import ModelActivity
from helpers import get_standard_response
# from api.custom_decorators import authentication_required


contact = ModelActivity('Contact')
contact_model = contact.get_operator()

standard_response = {
    'status': 'success'
}


@csrf_exempt
@require_http_methods(["POST"])
def create(request):
    # TODO: create custom decorator for authentication check
    try:
        token = request.POST['token']  # Will give Multidicterror if token key is missing
        Token.objects.get(key=token)  # Will give DoesNotExist if token is invalid
    except Exception as e:
        return ("User is unathenticated")

    new_data_for_contact = {
        'name': request.POST['name'],
        'email': request.POST['email']
    }
    try:
        contact = contact_model.create(**new_data_for_contact)
        response = get_standard_response(contact, many=False)
    except IntegrityError as e:
        response = get_standard_response(None, status='failed', message=e.message)
    return response


@require_http_methods(['GET'])
def read(request):
    data = {
        'search_keyword': request.GET['search']
    }

    contact = contact_model.read(**data)
    return get_standard_response(contact, many=True)


@csrf_exempt
@require_http_methods(['POST'])
def update(request):
    # TODO: Create custom decorator for authentication check
    try:
        token = request.POST['token']  # Will give Multidicterror if token key is missing
        Token.objects.get(key=token)  # Will give DoesNotExist if token is invalid
    except Exception as e:
        return ("User is unathenticated")
    # search_keyword here must uniquely identify the contact object in this case primary key/ Email
    data = {
        'search_keyword': request.POST['contact'],
        'name': request.POST['name'],
        'email': request.POST['email'],
    }
    try:
        contact = contact_model.update(**data)
        response = get_standard_response(contact)
    except (ValueError, ValidationError) as e:
        response = get_standard_response(None, status='failed', message=e.message)
    return response

@csrf_exempt
@require_http_methods(['POST'])
def delete(request):
    # TODO: Create custom decorator for authentication check
    try:
        token = request.POST['token'] # Will give Multidicterror if token key is missing
        Token.objects.get(key=token) # Will give DoesNotExist if token is invalid
    except Exception as e:
        return ("User is unathenticated")

    data = {
        'search_keyword': request.POST['contact'],
    }
    try:
        contact_model.delete(**data)
        response = get_standard_response(None)
    except ValueError as e:
        response = get_standard_response(None, status='failed', message=e.message)
    return response