import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from blog.models import Catgory
from datetime import datetime


@pytest.fixture
def client_fix():
    return APIClient()


@pytest.fixture
def client_with_token():
    user = get_user_model().objects.create_user(
        email="testuser@test.com", password="testpass", is_active=True
    )

    client = APIClient()
    response = client.post('/accounts/api/v2/jwt/create/', {
        'email': 'testuser@test.com',
        'password': 'testpass'
    }, format='json')

    assert response.status_code == 200
    access_token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    return client


@pytest.mark.django_db
class TestPostApi:
    def test_get_post_login_response_200(self, client_with_token):
        url = reverse("blog:api-v1:post-list")
        response = client_with_token.get(url)
        assert response.status_code == 200

    def test_creating_user_status_401(self, client_fix):
        url = reverse("blog:api-v1:post-list")
        catgory = Catgory.objects.create(name='test_category')
        data = {
            'author': 'test_author',
            'title': 'test_title',
            'content': 'this is test content',
            'status': True,
            'catgory': catgory.id,
            'published_date': datetime.now()
        }
        response = client_fix.post(url, data, format='json')
        assert response.status_code == 401
    