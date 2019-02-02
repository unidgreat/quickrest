from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework_jwt.settings import api_settings

from django.contrib.auth import get_user_model

from posting.models import BlogPost

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER
User = get_user_model()

class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User(username='testusername', email='test@email.com')
        user_obj.set_password("somethingsha")
        user_obj.save()

        blog_post = BlogPost.objects.create(
            # user=user_obj, 
            title="The test title", 
            content="the test blog post content"
            )

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_post(self):
        post_count = BlogPost.objects.count()
        self.assertEqual(post_count, 1)

    def test_get_list(self):
        data = {}
        url = api_reverse('api-posting:postings')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_blog(self):
        data = {'title':'A new title', 'content': 'The test post content'}
        url = api_reverse('api-posting:postings')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_single_blog_post(self):
        blog_post = BlogPost.objects.first()
        data = {}
        url = blog_post.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_blog_post(self):
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        data = {'title':'The update post title', 'content': 'This is another post for test. Make sense'}

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
    def test_update_blog_post_with_user(self):
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)

        data = {'title':'The update post title', 'content': 'This is another post for test. Make sense'}

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_blog_post_with_user(self):
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        
        data = {'title':'The new post title', 'content': 'This is another sense'}
        url = api_reverse('api-posting:postings')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_user_login(self):
        data = {'username': 'testusername', 'password': 'somethingsha'}
        url = api_reverse('api-login')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token')
        if token:
            blog_post = BlogPost.objects.first()
            url = blog_post.get_api_url()
            data = {'title':'New update post title', 'content': 'This is a new post update'}

            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
