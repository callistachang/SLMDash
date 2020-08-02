def test_index_page(app, client):
    res = client.get("/")
    assert res.status_code == 200


def test_dashboard_page(app, client):
    res = client.get("/dashboard/")
    assert res.status_code == 200


def test_data_report_page(app, client):
    res = client.get("/data-report/")
    assert res.status_code == 200


def test_ml_report_page(app, client):
    res = client.get("/ml-report/")
    assert res.status_code == 200
