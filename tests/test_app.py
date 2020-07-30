def test_index_page(app, client):
    res = client.get("/")
    assert res.status_code == 200


def test_dataviz_page(app, client):
    res = client.get("/dataviz/")
    assert res.status_code == 200
