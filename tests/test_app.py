def test_index_page(app, client):
    res = client.get("/")
    assert res.status_code == 200


def test_data_dashboard_page(app, client):
    res = client.get("/data-dashboard/")
    assert res.status_code == 200


def test_ml_dashboard_page(app, client):
    res = client.get("/ml-dashboard")
    assert res.status_code == 200


def test_data_report_page(app, client):
    res = client.get("/data-report")
    assert res.status_code == 200


def test_ml_report_page(app, client):
    res = client.get("/ml-report")
    assert res.status_code == 200
