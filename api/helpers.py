from django.http import JsonResponse
from api.serializers import ContactSerializer

def get_standard_response(data, many=False, status='success', message=''):
    serializer = ContactSerializer(data, many=many)
    standard_response = {
        'status': status,
        'message': message,
        'data': serializer.data
    }
    return JsonResponse(standard_response)