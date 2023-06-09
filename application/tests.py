import uuid
import datetime

from django.test import Client

from django.test import TestCase
from application.models import UserList, Shoppinglist
from django.contrib.auth.models import User
# Create your tests here.



class UserTestCase(TestCase):
    def setUp(self):
        self.user_name1 = 'user_1'
        self.user_email1 = 'user_1@gmail.com'
        self.user_password1 = 'passuser1'
        self.user_name2 = 'user_2'
        self.user_email2 = 'user_2@gmail.com'
        self.user_password2 = 'passuser2'

        user_1 = User.objects.create_user(self.user_name1, self.user_email1, self.user_password1)
        shoppinglist_user1 = UserList(id=user_1.id, list_id=uuid.uuid4())
        user_1.save()
        shoppinglist_user1.save()

        user_2 = User.objects.create_user(self.user_name2, self.user_email2, self.user_password2)
        shoppinglist_user2 = UserList(id=user_2.id, list_id=uuid.uuid4())
        user_2.save()
        shoppinglist_user2.save()

        self.user1_id = user_1.id
        self.user2_id = user_2.id

    def test_user_list_id_mapping(self):
        user = Client()
        user.login(username=self.user_name1, password=self.user_password1)
        response = user.post('/user/invate', {'email': self.user_email2})
        self.assertEqual(response.status_code, 200)

        user_list1 = UserList.objects.filter(id=self.user1_id).first()

        user_list2 = UserList.objects.filter(id=self.user2_id).first()

        self.assertEqual(user_list2.list_id, user_list1.list_id)

    def test_user_not_exsist(self):
        user = Client()
        user.login(username=self.user_name2, password=self.user_password2)
        response = user.post('/user/invate/', {'email': 'user3@gmail.com'})
        self.assertEqual(response.status_code, 404)


class UserRegister(TestCase):
    def createuser(self):
        user = Client()
        response = user.post('/user/register',
                             {'username': 'user_3', 'email': 'user3@gmail.com', 'password': 'passuser3'})
        user3 = User.objects.filter(username='user_3').first()
        self.assertIsNotNone(user3)
        user3_list = UserList.objects.filter(id=user3.id).first()
        self.assertIsNotNone(user3_list)

        response = user.post('/user/register',
                             {'username': 'user_4', 'email': 'user4@gmail.com', 'password': 'passuser4'})
        user4 = User.objects.filter(username='user_4').first()
        self.assertIsNotNone(user4)
        user4_list = UserList.objects.filter(id=user4.id).first()
        self.assertIsNotNone(user4_list)

        self.assertNotEqual(user3_list.list_id, user4_list.list_id)


class BuyItem(TestCase):
    fixtures = ['fixture_file.json']

    def test_buy_item(self):
        shoppinglist_user = Shoppinglist.objects.filter(list_id='199f4b29-c369-4543-893b-913738076321').first()
        user = Client()
        user.login(username='user_2', password='2222')

        response = user.post('/shoppinglist/<item_id>/buy', {'item': 17})
        self.assertEqual(response.status_code, 302)
        shoppinglist_user_coffe = Shoppinglist.objects.filter(list_id='199f4b29-c369-4543-893b-913738076321').first()
        self.assertEqual('bought', shoppinglist_user_coffe.status)
        self.assertEqual(datetime.date(2023, 3, 4), shoppinglist_user_coffe.buy_date)

        response = user.post('/shoppinglist/<item_id>/buy', {'item': 18})
        self.assertEqual(response.status_code, 302)
        shoppinglist_user_cottage_cheese = Shoppinglist.objects.filter(list_id='199f4b29-c369-4543-893b-913738076321').first()
        self.assertEqual('bought', shoppinglist_user_cottage_cheese.status)
        self.assertEqual(datetime.date(2023, 3, 4), shoppinglist_user_cottage_cheese.buy_date)





