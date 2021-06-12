import pytest

from app import ic
from app.auth import UserMod



# @pytest.mark.focus
def test_blank(tempdb, loop, client):
    async def ab():
        await tempdb()
        # x = await UserMod.all().values_list('email', flat=True)
        # ic(x)
    loop.run_until_complete(ab())

@pytest.mark.demopages
# @pytest.mark.skip
def test_public_page(tempdb, loop, client):
    async def ab():
        await tempdb()
    loop.run_until_complete(ab())
    
    res = client.get('/demo/public')
    data = res.json()
    # ic(data)
    assert res.status_code == 200
    assert data == 'public'

@pytest.mark.demopages
# @pytest.mark.skip
def test_private_page_auth(tempdb, loop, client, passwd, auth_headers_tempdb):
    headers, *_ = auth_headers_tempdb
    
    res = client.get('/demo/private', headers=headers)
    data = res.json()
    # ic(data)
    assert res.status_code == 200
    assert data == 'private'

@pytest.mark.demopages
# @pytest.mark.skip
def test_private_page_noauth(tempdb, loop, client):
    async def ab():
        await tempdb()
    loop.run_until_complete(ab())
    
    res = client.request('GET', '/demo/private')
    data = res.json()
    # ic(data)
    assert res.status_code == 401
    assert data.get('detail') == 'Unauthorized'