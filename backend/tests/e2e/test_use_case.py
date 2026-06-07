import pytest

@pytest.mark.e2e
@pytest.mark.asyncio
def docs_test(client):
    docs_response = await client.get('/docs')
    assert docs_response.status_code == 200