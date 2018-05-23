from api.models import Contact
from django.db.models import Q


class ContactActivity():

    def __init__(self, *args, **kwargs):
        self._all_field_names = [field.name for field in Contact._meta.get_fields()]

    def _remove_unnecessary_fields_from_kwargs(self, **kwargs):
        for key in kwargs.keys():
            if key.lower() not in self._all_field_names:
                kwargs.pop(key)
        return kwargs

    def create(self, *args, **kwargs):
        contact_object = Contact(**kwargs)
        contact_object.save()
        return contact_object

    def read(self, *args, **kwargs):
        search_keyword = kwargs['search_keyword']
        contacts = Contact.objects.filter(Q(email=search_keyword) | Q(name=search_keyword))
        return contacts

    def update(self, *args, **kwargs):
        contacts = self.read(**kwargs)
        if len(contacts)>1 or len(contacts)==0:
            raise ValueError("Could not identify or find a unique contact. Aborting")
        contact = contacts[0]
        update_fields = self._remove_unnecessary_fields_from_kwargs(**kwargs)
        for (key, value) in update_fields.items():
            setattr(contact, key, value)
        contact.save()
        return contact

    def delete(self, *args, **kwargs):
        contacts = self.read(**kwargs)
        if len(contacts)>1 or len(contacts)==0:
            raise ValueError("Could not identify or find a unique contact. Aborting")
        contact = contacts[0]
        contact.delete()


class ModelActivity(object):
    model_to_helper_mapping = {
        'Contact': ContactActivity()
    }

    def __init__(self, table_name):
        self.table_name = table_name

    def create(self, *args, **kwargs):
        raise NotImplementedError("Method not implement to support this action")

    def read(self, *args, **kwargs):
        raise NotImplementedError("Method not implement to support this action")

    def update(self, *args, **kwargs):
        raise NotImplementedError("Method not implement to support this action")

    def remove(self, *args, **kwargs):
        raise NotImplementedError("Method not implement to support this action")

    def get_operator(self, *args, **kwargs):
        if self.table_name in self.model_to_helper_mapping:
            return self.model_to_helper_mapping.get(self.table_name)
            # return self._str_to_class(self.model_to_helper_mapping[self.table_name])
        raise ValueError("Unknown table requested for operation")
