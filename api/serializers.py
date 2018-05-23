from rest_framework import serializers
from api.models import Contact

class ContactSerializer(serializers.ModelSerializer):
    """
    Serializes contact model into json format.
    """

    class Meta:
        model = Contact
        fields = ('id', 'name', 'email')
