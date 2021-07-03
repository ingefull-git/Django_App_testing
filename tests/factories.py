import factory
from django.contrib.auth.models import User
from faker import Faker

from apps.logchecker.models import District

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.name()
    password = "1234567890"
    first_name = fake.first_name()


class DistrictFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = District

    user = factory.SubFactory(UserFactory)
    name = fake.name()
    psid = 12345