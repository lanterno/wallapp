from rest_framework.test import APITestCase
from django.urls import reverse

from wallapp.accounts.tests.factories import UserFactory

from .. import settings
from ..models import Post


class PostTests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()

    def test_only_authenticated_users_can_create_posts(self):
        posts_count_before = Post.objects.count()
        # unauthentcated user -> try to create a post
        response = self.client.post(
            reverse('wall:posts-list'),
            data={
                'text': "This is my first Post"
            }
        )
        self.assertEqual(response.status_code, 401)

        # test authenticated users can create posts
        self.client.login(email=self.user.email, password='123qwe')
        response = self.client.post(
            reverse('wall:posts-list'),
            data={
                'text': "This is my first Post"
            }
        )
        self.assertEqual(response.status_code, 201)
        posts_count_now = Post.objects.count()
        self.assertEqual(posts_count_before + 1, posts_count_now)

    def test_only_owner_can_update_his_post(self):
        self.client.login(email=self.user.email, password='123qwe')
        response = self.client.post(
            reverse('wall:posts-list'),
            data={
                'text': "This is my first Post"
            }
        )
        post = Post.objects.last()

        # check other users can't update post
        self.client.login(email=self.other_user.email, password='123qwe')
        response = self.client.put(
            reverse('wall:posts-detail', args=[post.pk]),
            data={
                'text': "This is my first updated Post"
            }
        )
        self.assertEqual(response.status_code, 403)

        # check owner can update post
        self.client.login(email=self.user.email, password='123qwe')
        response = self.client.put(
            reverse('wall:posts-detail', args=[post.pk]),
            data={
                'text': "This is my first updated Post"
            }
        )
        self.assertEqual(response.status_code, 200)

        # test other users can't delete post
        self.client.login(email=self.other_user.email, password='123qwe')
        response = self.client.delete(
            reverse('wall:posts-detail', args=[post.pk]),
            data={
                'text': "This is my first updated Post"
            }
        )
        self.assertEqual(response.status_code, 403)

        # check owner can update post
        self.client.login(email=self.user.email, password='123qwe')
        response = self.client.delete(
            reverse('wall:posts-detail', args=[post.pk]),
            data={
                'text': "This is my first updated Post"
            }
        )
        self.assertEqual(response.status_code, 204)

    def test_post_max_length(self):
        max_length = settings.POST_MAX_LENGTH
        post = "A" * max_length + "X"
        self.client.login(email=self.user.email, password='123qwe')
        response = self.client.post(
            reverse('wall:posts-list'),
            data={
                'text': post
            }
        )
        self.assertEqual(response.status_code, 400)


class WallUserInteraction(APITestCase):

    def test_anyone_can_list_posts_on_wall(self):
        '''
        Get only newest 10 posts
        - can pagniate through the rest of results
        '''
