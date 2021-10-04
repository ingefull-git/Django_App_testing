from django.contrib.auth.models import User
import pytest
from pytest_factoryboy import register
from tests.factories import DistrictFactory, UserFactory
from apps.logchecker.models import District

register(UserFactory)
register(DistrictFactory)

@pytest.fixture
def fixt1(db):
    user1 = User.objects.create_user(username="rulotest1")
    return user1

@pytest.fixture
def fixt_factory(db):
    def create_app_user(
        username: str,
        password: str = None,
        first_name: str = "firstname1"
        ):
        user = User.objects.create(
            username = username,
            password =password,
            first_name = first_name
        )
        return user
    return create_app_user

@pytest.fixture
def new_user(fixt_factory):
    return fixt_factory("test_user_01", "password_01", "user_name_01")

@pytest.fixture
def new_user2(db, user_factory):
    user = user_factory.create()
    return user

@pytest.fixture
def new_district(db, district_factory):
    district = district_factory.create()
    return district

@pytest.fixture
def distr_factory(db, new_user2):
    def create_district(
        user_id: int,
        name: str = None,
        psid: int = None
        ):
        district = District.objects.create(
            user_id = new_user2.psid,
            name = name,
            psid = psid
        )
        return district
    return create_district

@pytest.fixture
def new_distr(distr_factory):
    return distr_factory(2,"District_01", "12345")