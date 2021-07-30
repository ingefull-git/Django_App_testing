from django.contrib.auth.models import User
from django.test import TestCase
from mixer.backend.django import mixer
from apps.logchecker.models import District
import pytest

class TestModelDistrict(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username="rulito")
        cls.dist1 = District.objects.create(user=cls.user1, name="District1", psid="111111")
        print("Setup Class")

    def test_district_name(self):
        assert self.dist1.name == "District1"
        
    def test_district_psid(self):
        assert self.dist1.psid == "111111"

    def test_district_str(self):
        assert self.dist1.name in str(self.dist1)
        assert self.dist1.psid in str(self.dist1)
        assert str(self.dist1) == "District1 PSID: 111111"

    def test_district_user_instance(self):
        assert isinstance(self.dist1.user, User)

    def test_district_user_name(self):
        username = self.user1.username
        assert username == "rulito"

class TestModel(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username="rulito")
        self.dist1 = District.objects.create(user=self.user1, name="District1", psid="111111")
        print("Setup Func")

    def test_model_name(self):
        assert self.dist1.name == "District1"
        
    def test_model_psid(self):
        assert self.dist1.psid == "111111"

    def test_model_001(self):
        assert self.dist1.name in str(self.dist1)
        assert self.dist1.psid in str(self.dist1)
        assert str(self.dist1) == "District1 PSID: 111111"

    def test_district_user_instance(self):
        assert isinstance(self.dist1.user, User)

    def test_district_user_name(self):
        username = self.user1.username
        assert username == "rulito"


def test_example1(fixt1):
    user_t1 = fixt1
    assert user_t1.username == "rulotest1" 

def test_new_user01(new_user):
    assert new_user.first_name == "user_name_01"

def test_new_user02(new_user2):
    user = new_user2
    print(user.psid, " + ", user.username, " + ", user.first_name, " + ", user.password)
    assert True

def test_district_01(new_district):
    dist = new_district
    print(dist.user_id, " + ", dist.name, " + ", dist.psid)
    assert isinstance(dist.user, User)

def test_district_02(new_distr):
    dist = new_distr
    print(dist.user_id, " + ", dist.name, " + ", dist.psid)
    assert isinstance(dist.user, User)

@pytest.mark.parametrize(
    "user, name, psid, valid",
    [
        (1, "District_01", 123456, True), # all the data correct
        # ("", "D1", 123, False), # without user_id field
        (1, "", 123, True), # without name field
        # (1, "D1", "", 1), # without psid field
    ],
)
def test_district_03(db,district_factory, user, name,psid,valid):
    test = district_factory(
        user_id=user,
        name=name,
        psid=psid,
    )
    dist = District.objects.all().count()
    dist1 = District.objects.first()
    # dist2 = District.objects.create(psid=123)
    print(dist1.user_id, dist1.name, dist1.psid)
    print(dist, valid)
    assert dist == valid

def test_district_04(db):
    dist01 = mixer.blend('logchecker.District', name='District_001', psid=12345)
    assert dist01.name == "District_001"
    assert dist01.psid == 12345

