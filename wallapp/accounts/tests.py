from rest_framework.test import APITestCase
from django.urls import reverse

from .models import User
from .factories import UnactivatedUserFactory, ActivatedUserFactory, ClosedAccountFactory


class UserTests(APITestCase):

    def test_user_registration_flow(self):
        # test system has no users
        self.assertEqual(User.objects.all().count(), 0)
        # test user signup
        response = self.client.post(
            reverse('auth:register'),
            data={
                'email': 'cal@krypton.com',
                'password': '123qwe'
            }
        )
        self.assertEqual(response.status_code, 201)
        # test user exists
        self.assertEqual(User.objects.all().count(), 1)

        # test user can't login
        response = self.client.post(
            reverse('auth:login'),
            data={
                'email': 'cal@krypton.com',
                'password': '123qwe'
            }
        )
        self.assertEqual(response.status_code, 400, response.content)

        # Activate user manually until we find a way to test emails
        user = User.objects.first()
        user.is_active = True
        user.save()

        # test user can login after activation
        response = self.client.post(
            reverse('auth:login'),
            data={
                'email': 'cal@krypton.com',
                'password': '123qwe'
            }
        )
        self.assertEqual(response.status_code, 200, response.content)

    def test_user_can_login_and_see_profile(self):
        user = ActivatedUserFactory.create()
        response = self.client.post(
            reverse('auth:login'),
            data={
                'email': user.email,
                'password': '123qwe'
            }
        )
        self.assertEqual(response.status_code, 200)
        token = 'Token ' + response.json()['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION=token)
        # Now, user should be logged-in
        response = self.client.get(
            reverse('auth:user'),
        )
        self.assertEqual(response.status_code, 200)

    def test_loggedin_user_can_disable_account(self):
        user = ActivatedUserFactory.create()
        self.client.login(email=user.email, password='123qwe')
        # Now, user should be logged-in

        response = self.client.post(
            reverse('auth:disable_account')
        )
        self.assertEqual(response.status_code, 200)
        # call it again to make sure user isn't authenticated anymore
        response = self.client.post(
            reverse('auth:disable_account')
        )
        self.assertEqual(response.status_code, 401)

    def test_user_can_reactivate_account(self):
        user = ClosedAccountFactory()

        # test user can't login
        self.assertFalse(self.client.login(email=user.email, password='123qwe'))

        # call login with activate=True
        response = self.client.post(
            reverse('auth:login'),
            data={
                'email': user.email,
                'password': '123qwe',
                'activate': True
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_unverified_users_cant_activate_their_accounts_illegally(self):
        """
        This is to test that unverified users can't login by setting
        activate=True
        """
        user = UnactivatedUserFactory()

        # call login with activate=True
        response = self.client.post(
            reverse('auth:login'),
            data={
                'email': user.email,
                'password': '123qwe',
                'activate': True
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_unverified_users_and_closed_accounts_get_different_error_messages(self):
        unactivated_user = UnactivatedUserFactory()
        closed_account = ClosedAccountFactory()

        response1 = self.client.post(
            reverse('auth:login'),
            data={
                'email': unactivated_user.email,
                'password': '123qwe',
            }
        ).json()

        response2 = self.client.post(
            reverse('auth:login'),
            data={
                'email': closed_account.email,
                'password': '123qwe',
            }
        ).json()

        self.assertNotEqual(response1, response2)
