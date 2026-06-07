import pytest
from unittest.mock import Mock 


@pytest.mark.unit
def client_test(client):
    response = await client.get('/health')
    assert response.status_code == 200
    assert response.json() = {'status':'ok'}

