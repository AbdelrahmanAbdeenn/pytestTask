from unittest import mock
from unittest.mock import Mock
import pytest
from requests import HTTPError, Response, patch
import requests


from app import get_post_by_id, get_posts_by_user_id , get_post_by_id_with_validation



def test_get_post_by_id(mocker):
    
    mock_response = Mock(spec=Response)
    mock_response.status_code = 200
    
    mock_response.json.return_value = {
        'userId': 1,
        'id': 1,
        'title': 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit',
        'body': 'quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto'
    }
    
    mocker.patch('app.http_get', return_value=mock_response)
    result = get_post_by_id(1)
        
    assert result == {
                'userId': 1,
                'id': 1,
                'title': 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit',
                'body': 'quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto'
    }
            
def test_get_posts_by_user_id_http_error(mocker):
    # Simulate an HTTP error
    mocker.patch('app.http_get', side_effect=HTTPError("HTTP error occurred"))

    result = get_posts_by_user_id(1)
    
    assert result is None


def test_get_posts_by_user_id(mocker):
    # Create a mock response object
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
    
    mocker.patch('app.http_get', return_value=mock_response)
       
    result = get_posts_by_user_id(1)
        
    assert result == [
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

def test_get_post_by_id_with_validation(mocker):
    
    mock_response = Mock(spec=Response)
    mock_response.status_code = 200
    
    mock_response.json.return_value = {
        'userId': 1,
        'id': 1,
        'title': 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit',
        'body': 'quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto'
    }
    
    mocker.patch('app.http_get', return_value=mock_response)
    result = get_post_by_id_with_validation(1)
        
    assert result == {
                'userId': 1,
                'id': 1,
                'title': 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit',
                'body': 'quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto'
            }
        
def test_get_post_by_id_with_validation_http_error(mocker):

    mocker.patch('app.http_get', side_effect=HTTPError("HTTP error occurred"))

    result = get_post_by_id_with_validation(1)
    
    assert result is None

def test_get_post_by_id_with_validation_invalid_id():
    with pytest.raises(ValueError):
        get_post_by_id_with_validation(0)
