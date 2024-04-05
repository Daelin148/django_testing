# news/tests/test_logic.py
from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from pytest_django.asserts import assertFormError, assertRedirects

User = get_user_model()
COMMENT_TEXT = 'Текст комментария'
NEW_COMMENT_TEXT = 'Обновлённый комментарий'
COMMENT_FORM = {'text': COMMENT_TEXT}
pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(client, news_detail_url):
    client.post(news_detail_url, data=COMMENT_FORM)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(
    news_detail_url, author_client, author, news, url_to_comments
):
    response = author_client.post(news_detail_url, data=COMMENT_FORM)
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_TEXT
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, news_detail_url):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(news_detail_url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(
        author_client, comment_delete_url, url_to_comments
):
    response = author_client.delete(comment_delete_url)
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(
    not_author_client, comment_delete_url
):
    response = not_author_client.delete(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(
    author_client, comment_edit_url, url_to_comments, comment
):
    COMMENT_FORM['text'] = NEW_COMMENT_TEXT
    response = author_client.post(comment_edit_url, data=COMMENT_FORM)
    assertRedirects(response, url_to_comments)
    comment = Comment.objects.get()
    assert comment.text == NEW_COMMENT_TEXT


def test_user_cant_edit_comment_of_another_user(
    not_author_client, comment, comment_edit_url
):
    response = not_author_client.post(comment_edit_url, data=COMMENT_FORM)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment = Comment.objects.get()
    assert comment.text == COMMENT_TEXT
