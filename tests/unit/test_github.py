# -*- coding: utf-8 -*-
from evenflow.Github import Github
from evenflow.Http import Http
from evenflow.Jwt import Jwt
from evenflow.models import Users

from pytest import fixture, mark


@fixture
def user():
    return Users('name', 'email', '@handle')


@fixture
def gh(user):
    return Github('123456789', 'github.pem', 'organization')


@fixture
def headers():
    return {'Authorization': 'Bearer token',
            'Accept': 'application/vnd.github.machine-man-preview+json'}


def test_github(user, gh):
    assert gh.api_url == 'https://api.github.com'
    assert gh.github_app == '123456789'
    assert gh.github_pem == 'github.pem'
    assert gh.organization == 'organization'


@mark.parametrize('page, url', [
    ('repository', 'repos/{}/{}/contents'),
    ('installations', 'installations/{}/access_tokens')
])
def test_github_url_repository(gh, page, url):
    expected = '{}{}'.format('https://api.github.com/', url)
    assert gh.url(page) == expected


def test_github_url_none(gh):
    assert gh.url('magic') is None


def test_github_make_url(mocker, gh):
    mocker.patch.object(Github, 'url', return_value='test/{}')
    result = gh.make_url('page', 'argument')
    Github.url.assert_called_with('page')
    assert result == 'test/argument'


def test_get_token(mocker, gh, headers):
    mocker.patch.object(Http, 'post')
    mocker.patch.object(Jwt, 'encode', return_value='token')
    mocker.patch.object(Github, 'make_url')
    result = gh.get_token()
    Jwt.encode.assert_called_with(gh.github_pem, 500, iss=gh.github_app)
    args = {'transformation': 'json', 'headers': headers}
    Http.post.assert_called_with(Github.make_url(), **args)
    assert result == Http.post()['token']


def test_get_contents(mocker, gh, headers):
    mocker.patch.object(Http, 'get')
    mocker.patch.object(Github, 'make_url')
    mocker.patch.object(Github, 'get_token', return_value='token')
    result = gh.get_contents('org', 'repo', 'file')
    Github.make_url.assert_called_with('repository', 'org', 'repo', 'file')
    Http.get.assert_called_with(Github.make_url(), transformation='base64',
                                params={'ref': None}, headers=headers)
    assert Github.get_token.call_count == 1
    assert result == Http.get()


def test_get_contents_version(mocker, gh, headers):
    mocker.patch.object(Http, 'get')
    mocker.patch.object(Github, 'make_url')
    mocker.patch.object(Github, 'get_token', return_value='token')
    gh.get_contents('org', 'repo', 'file', 'version')
    Http.get.assert_called_with(Github.make_url(), transformation='base64',
                                params={'ref': 'version'}, headers=headers)
