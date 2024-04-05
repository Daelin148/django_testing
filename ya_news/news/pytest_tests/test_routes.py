from http import HTTPStatus

import pytest
from django.test import Client
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db

HOME_URL = pytest.lazy_fixture(
    'home_url'
)
DETAIL_URL = pytest.lazy_fixture('news_detail_url')
EDIT_URL = pytest.lazy_fixture('comment_edit_url')
DELETE_URL = pytest.lazy_fixture('comment_delete_url')
LOGIN_URL = pytest.lazy_fixture('login_url')
LOGOUT_URL = pytest.lazy_fixture('logout_url')
SIGNUP_URL = pytest.lazy_fixture('signup_url')
EDIT_URL_REDIRECT = pytest.lazy_fixture('edit_url_redirect')
DELETE_URL_REDIRECT = pytest.lazy_fixture('delete_url_redirect')
ANONYM_CLIENT = Client()
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')


@pytest.mark.parametrize(
    'url, redirect_url', (
        (EDIT_URL, EDIT_URL_REDIRECT),
        (DELETE_URL, DELETE_URL_REDIRECT),
    )
)
def test_redirect_for_anonymous_client(url, redirect_url, client):
    response = client.get(url)
    assertRedirects(response, redirect_url)


@pytest.mark.parametrize(
    'user, url, expected_status', (
        (ANONYM_CLIENT, HOME_URL, HTTPStatus.OK),
        (ANONYM_CLIENT, LOGIN_URL, HTTPStatus.OK),
        (ANONYM_CLIENT, DETAIL_URL, HTTPStatus.OK),
        (ANONYM_CLIENT, LOGOUT_URL, HTTPStatus.OK),
        (ANONYM_CLIENT, SIGNUP_URL, HTTPStatus.OK),
        (AUTHOR_CLIENT, EDIT_URL, HTTPStatus.OK),
        (AUTHOR_CLIENT, DELETE_URL, HTTPStatus.OK),
        (NOT_AUTHOR_CLIENT, EDIT_URL, HTTPStatus.NOT_FOUND),
        (NOT_AUTHOR_CLIENT, DELETE_URL, HTTPStatus.NOT_FOUND)
    )
)
def test_status_codes(user, expected_status, url):
    responce = user.get(url)
    assert responce.status_code == expected_status
