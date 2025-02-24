from typing import Any
from unittest.mock import Mock

import pytest
from requests import HTTPError, Response

from app import (get_post_by_id, get_post_by_id_with_validation,
                 get_posts_by_user_id)


def test_get_post_by_id(mocker) -> None:    
    mock_response :Mock = Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'userId': 1,
        'id': 1,
        'title': 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit',
        'body': 'quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto'
    }
    
    mock_get=mocker.patch('app.http_get', return_value=mock_response)
    result :dict[str,Any]| None = get_post_by_id(1)
    mock_get.assert_called_once_with('https://jsonplaceholder.typicode.com/posts/1')
    
            
def test_get_posts_by_user_id_http_error(mocker):
    mocker.patch('app.http_get', side_effect=HTTPError("HTTP error occurred"))
    result :dict[str,Any]| None= get_posts_by_user_id(1)
    assert result is None

def test_get_posts_by_user_id(mocker):
    mock_response = Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            'userId': '1',
            'id': '1',
            'title': 'Post title 1',
            'body': 'Post body content 1'
        },
        {
            'userId': '1',
            'id': '2',
            'title': 'Post title 2',
            'body': 'Post body content 2'
        }
    ]
    
    mock_get=mocker.patch('app.http_get', return_value=mock_response)
    result:dict[str,Any]| None = get_posts_by_user_id(1)
    mock_get.assert_called_once_with('https://jsonplaceholder.typicode.com/posts?userId=1')    
    

def test_get_post_by_id_with_validation(mocker):

    mock_response = Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'userId': 1,
        'id': 1,
        'title': 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit',
        'body': 'quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto'
    }
    
    mock_get=mocker.patch('app.http_get', return_value=mock_response)
    get_post_by_id_with_validation(1)
    mock_get.assert_called_once_with('https://jsonplaceholder.typicode.com/posts/1')

   
def test_get_post_by_id_with_validation_http_error(mocker):

    mocker.patch('app.http_get', side_effect=HTTPError("HTTP error occurred"))
    result :dict[str,Any]| None= get_post_by_id_with_validation(1)
    assert result is None

def test_get_post_by_id_with_validation_invalid_id():
    with pytest.raises(ValueError , match="Invalid ID"):
        get_post_by_id_with_validation(0)
    with pytest.raises(ValueError , match="post_id must be a positive number"):
        get_post_by_id_with_validation(-1)
