from flask import url_for


def test_index_page(client):
    res = client.get("/")
    assert res.status_code == 200
