import pytest
import requests
from unittest.mock import patch
from src.hh_api import HHVacancyAPIClient


class TestHHVacancyAPIClient:
    def setup_method(self):
        self.client = HHVacancyAPIClient()

    @patch('requests.get')
    def test_get_response_success(self, mock_get):
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response.json = lambda: {'items': [{'id': '1', 'name': 'Test Vacancy'}]}
        mock_get.return_value = mock_response

        response = self.client._HHVacancyAPIClient__get_response('python', 0, 100)
        assert response.status_code == 200
        assert response.json()['items'][0]['id'] == '1'
        assert response.json()['items'][0]['name'] == 'Test Vacancy'

    @patch('requests.get')
    def test_get_response_error(self, mock_get):
        mock_response = requests.Response()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with pytest.raises(Exception) as e:
            self.client._HHVacancyAPIClient__get_response('python', 0, 100)
        assert str(e.value) == "Error fetching data. Status code: 404"


if __name__ == "__main__":
    pytest.main()
